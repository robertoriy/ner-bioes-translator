from typing import Dict

import pandas as pd

from app.dependencies.dependencies import get_config_handler
from app.schemas.evaluations.back_translation_data import BackTranslationData
from app.schemas.evaluations.back_translation_evaluation import BackTranslationEvaluation
from app.schemas.evaluations.expert_evaluation_values import ExpertEvaluationValues
from app.schemas.evaluations.expert_evaluation import ExpertEvaluation
from app.schemas.sentences.bioes_tag import BioesTag
from app.schemas.sentences.plain_data import PlainData
from app.schemas.sentences.sentence import Sentence
from app.schemas.sentences.sentence_detail_base import SentenceDetailBase
from app.schemas.sentences.sentence_detail_translated import SentenceDetailTranslated
from app.schemas.sentences.sentence_short import SentenceShort


class DataFrameMapper:

    @classmethod
    def df_to_sentences_json(
            cls,
            df: pd.DataFrame,
            expert_evaluations: Dict[str, Dict[str, ExpertEvaluationValues]],
            back_translation_evaluations: Dict[str, Dict[str, BackTranslationEvaluation]]
    ):
        original_lang_code = get_config_handler().get_config().prompt_data.get_original_language()
        print("DF: ")
        print(df)
        print("Expert evaluations: ")
        print(expert_evaluations)

        original_sentences = {
            int(sent.split()[1]): ' '.join(str(word) if word is not None else "" for word in words)
            for sent, words in df.groupby('Sentence')[f'Word_original_{original_lang_code}']
        }

        result = []
        # todo back_translation_evaluations
        for sentence_id, lang_evaluation in expert_evaluations.items():
            expert_evaluation = [
                ExpertEvaluation(
                    language_code=lang,
                    evaluation=evaluation.value
                )
                for lang, evaluation in lang_evaluation.items()
            ]

            back_translation_evaluation = [
                BackTranslationData(
                    language_code=lang,
                    back_translated_sentence=evaluation.back_translated_sentence,
                    evaluation=evaluation.evaluation
                )
                for lang, evaluation in back_translation_evaluations.get(sentence_id, {}).items()
            ]

            sentence = SentenceShort(
                id=int(sentence_id),
                original_sentence=original_sentences.get(int(sentence_id)),
                expert_evaluation=expert_evaluation,
                back_translation_evaluation=back_translation_evaluation
            )
            result.append(sentence)
        return result

    @classmethod
    def df_to_sentence_json(
            cls,
            df: pd.DataFrame,
            sentence_id: int,
            expert_evaluations: Dict[str, Dict[str, ExpertEvaluationValues]],
            back_translation_evaluations: Dict[str, Dict[str, BackTranslationEvaluation]]
    ):
        needed_df = df[df['Sentence'] == f"Sentence {sentence_id}"]

        original_lang_code = get_config_handler().get_config().prompt_data.get_original_language()
        code = f"original_{original_lang_code}"
        original_sentence = cls.process_original_sentence(
            needed_df,
            code,
        )

        translated_sentence = []
        languages = set()
        for col in needed_df.columns:
            if col.startswith("Word_") and not col.endswith(f"_{original_lang_code}"):
                lang = col.split("_")[1]
                languages.add(lang)
        for lang in languages:
            translated_sentence.append(
                cls.process_common_sentence(
                    needed_df,
                    sentence_id,
                    lang,
                    expert_evaluations,
                    back_translation_evaluations
                )
            )

        return Sentence(
            id=sentence_id,
            original_sentence=original_sentence,
            translated_sentence=translated_sentence
        )

    @classmethod
    def process_original_sentence(
            cls,
            df: pd.DataFrame,
            suffix: str,
    ):
        config = get_config_handler().get_config().prompt_data
        language = config.get_extended_original_language()

        bioes = list(zip(df[f'Word_{suffix}'], df[f'BIOES-Tag_{suffix}']))
        full_sentence, content, named_entities = cls.parse_bioes(bioes)

        kwargs = {
            "language": language,
            "full_sentence": full_sentence,
            "named_entity": named_entities,
            "content": content
        }
        return SentenceDetailBase(
            language=language,
            full_sentence=full_sentence,
            named_entity=named_entities,
            content=content
        )

    @classmethod
    def process_common_sentence(
            cls,
            df: pd.DataFrame,
            sentence_id: int,
            suffix: str,
            expert_evaluations: Dict[str, Dict[str, ExpertEvaluationValues]],
            back_translation_evaluations: Dict[str, Dict[str, BackTranslationEvaluation]]
    ):
        config = get_config_handler().get_config().prompt_data
        language = config.get_extended_language(suffix)

        bioes = list(zip(df[f'Word_{suffix}'], df[f'BIOES-Tag_{suffix}']))

        full_sentence, content, named_entities = cls.parse_bioes(bioes)

        expert_evaluation = expert_evaluations[str(sentence_id)][suffix].value
        back_translation_evaluation = back_translation_evaluations[str(sentence_id)][suffix]

        return SentenceDetailTranslated(
            language=language,
            full_sentence=full_sentence,
            named_entity=named_entities,
            content=content,
            expert_evaluation=expert_evaluation,
            back_translation_evaluation=back_translation_evaluation
        )

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
