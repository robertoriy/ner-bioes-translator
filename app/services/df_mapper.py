from typing import Dict

import pandas as pd

from app.dependencies.dependencies import get_config_handler
from app.schemas.config.language import Language
from app.schemas.scores.score_values import ScoreValues
from app.schemas.scores.sentence_score import SentenceScore
from app.schemas.sentences.bioes_tag import BioesTag
from app.schemas.sentences.plain_data import PlainData
from app.schemas.sentences.sentence import Sentence
from app.schemas.sentences.sentence_detail import SentenceDetail
from app.schemas.sentences.sentence_short import SentenceShort
from app.services.evaluation_score_handler import scores


class DataFrameMapper:
    def __init__(self):
        pass

    @classmethod
    def df_to_sentences_json(cls, df: pd.DataFrame, scores: Dict[str, Dict[str, ScoreValues]]):
        original_lang_code = get_config_handler().get_config().prompt_data.get_original_language()
        print("DF: ")
        print(df)
        print("Scores: ")
        print(scores)

        original_sentences = {
            int(sent.split()[1]): ' '.join(str(word) if word is not None else "" for word in words)
            for sent, words in df.groupby('Sentence')[f'Word_original_{original_lang_code}']
        }

        result = []
        for sentence_id, lang_scores in scores.items():
            sentence_scores = [
                SentenceScore(
                    language_code=lang,
                    evaluation_score=score.value
                )
                for lang, score in lang_scores.items()
            ]

            sentence = SentenceShort(
                id=int(sentence_id),
                original_sentence=original_sentences.get(int(sentence_id)),
                evaluation_score=sentence_scores
            )
            result.append(sentence)
        return result

    @classmethod
    def df_to_sentence_json(cls, df: pd.DataFrame, sentence_id: int, scores: Dict[str, Dict[str, ScoreValues]]):
        needed_df = df[df['Sentence'] == f"Sentence {sentence_id}"]

        original_lang_code = get_config_handler().get_config().prompt_data.get_original_language()
        code = f"original_{original_lang_code}"
        original_sentence = cls.process_sentence(needed_df, sentence_id, code, scores)

        translated_sentence = []
        languages = set()
        for col in needed_df.columns:
            if col.startswith("Word_") and not col.endswith(f"_{original_lang_code}"):
                lang = col.split("_")[1]
                languages.add(lang)
        for lang in languages:
            translated_sentence.append(cls.process_sentence(needed_df, sentence_id, lang, scores))


        return Sentence(
            id=sentence_id,
            original_sentence=original_sentence,
            translated_sentence=translated_sentence
        )

    @classmethod
    def process_sentence(cls,
                         df: pd.DataFrame,
                         sentence_id: int,
                         suffix: str,
                         scores: Dict[str, Dict[str, ScoreValues]]
                         ):
        is_original = suffix.startswith('original')
        bioes = list(zip(df[f'Word_{suffix}'], df[f'BIOES-Tag_{suffix}']))

        config = get_config_handler().get_config().prompt_data
        if is_original:
            language = config.get_extended_original_language()
        else:
            language = config.get_extended_language(suffix)

        full_sentence, content, named_entities = cls.parse_bioes(bioes)

        kwargs = {
            "language": language,
            "full_sentence": full_sentence,
            "named_entity": named_entities,
            "content": content
        }
        if not is_original:
            kwargs["evaluation_score"] = scores[str(sentence_id)][suffix].value
        return SentenceDetail(**kwargs)

    @classmethod
    def parse_bioes(cls, bioes):
        full_sentence = ''
        content = []
        named_entity = []
        current_entity = []

        for word, tag in bioes:
            if pd.isna(word) or pd.isna(tag):
                continue

            full_sentence = full_sentence + ' ' + word

            prefix, tag_type = tag.split("-") if "-" in tag else (tag, "")
            content.append(PlainData(
                word=str(word),
                tag=BioesTag(
                    full_tag=tag,
                    prefix=prefix,
                    type=tag_type
                )
            ))

            if tag == 'O':
                if current_entity:
                    named_entity.append((' '.join(current_entity)))
                    current_entity = []
                continue

            if prefix == 'B':
                if current_entity:
                    named_entity.append((' '.join(current_entity)))
                current_entity = [word]
            elif prefix == 'I':
                if current_entity:
                    current_entity.append(word)
            elif prefix == 'E':
                if current_entity:
                    current_entity.append(word)
                    named_entity.append((' '.join(current_entity)))
                    current_entity = []
            elif prefix == 'S':
                if current_entity:
                    named_entity.append((' '.join(current_entity)))
                named_entity.append(word)
                current_entity = []

        if current_entity:
            named_entity.append((' '.join(current_entity)))

        named_entity = [item for item in named_entity if item[0]]

        full_sentence = full_sentence.strip()

        return full_sentence, content, named_entity

