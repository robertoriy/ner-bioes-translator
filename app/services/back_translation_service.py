import pandas as pd
from openai import OpenAI

from app.handlers.back_translation_evaluation_handler import back_translation_evaluations
from app.schemas.config.service_config import ServiceConfig
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.evaluations.back_translation_evaluation import BackTranslationEvaluation
from config import settings


class BackTranslationService:
    def __init__(self):
        self._client = OpenAI(
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
        )
        self._model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def make_evaluation(self, df: pd.DataFrame, config: ServiceConfig):

        model = config.model
        prompt_config = config.prompt_data
        languages = prompt_config.get_languages()

        for language_code in languages:
            role, task = prompt_config.get_back_translation_role_and_task(language_code)

            sentences = (df.groupby('Sentence')[f'Word_{language_code}']
                         .apply(lambda x: ' '.join(word for word in x if word is not None))
                         .to_dict())
            for sentence_id, sentence in sentences.items():
                back_translated_sentence = self.translate(sentence, model, role, task)
                original_sentence = back_translation_evaluations.get_original_sentence(sentence_id.split()[1])

                evaluation = self.evaluate(original_sentence, back_translated_sentence)

                back_translation_evaluations.update(
                    sentence_id.split()[1],
                    language_code,
                    BackTranslationEvaluation(
                        original_sentence=original_sentence,
                        back_translated_sentence=back_translated_sentence,
                        evaluation=evaluation,
                    )
                )

        return back_translation_evaluations

    def translate(self, sentence: str, model: str, role: str, task: str):
        task = task + ' ' + sentence

        chat_completion = self._client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": role
                },
                {
                    "role": "user",
                    "content": task
                }
            ],
            temperature=0.3
        )
        print(chat_completion)
        result = chat_completion.choices[0].message.content
        print(f"Обработка запроса {sentence} | \nперевод - {result}")
        return result

    def evaluate(self, original_sentence, back_translated_sentence):
        emb_original = self._model.encode(original_sentence)
        emb_reverse = self._model.encode(back_translated_sentence)
        similarity = cosine_similarity(emb_original.reshape(1, -1), emb_reverse.reshape(1, -1))[0][0]
        return similarity


back_translator = BackTranslationService()
