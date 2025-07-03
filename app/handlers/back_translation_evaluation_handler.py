from typing import Dict, List, Optional

from app.schemas.evaluations.back_translation_evaluation import BackTranslationEvaluation
from app.schemas.evaluations.back_translation_evaluations import BackTranslationEvaluations


class BackTranslationEvaluationHandler:
    def __init__(self):
        self.back_translations: Dict[str, Dict[str, BackTranslationEvaluation]] = {}
        # {sentence_id: {language: {back_translation}}}
        self.target_languages: Optional[List[str]] = None

    def initialize(
            self,
            sentences: Dict[str, str],
            target_languages: List[str],
            default_evaluation: float = 0.0
    ):
        """Инициализация с дефолтными значениями для всех языков"""
        self.target_languages = target_languages
        self.back_translations = {
            sentence_id.split()[1]: {
                language: BackTranslationEvaluation(
                    original_sentence=original_sentence,
                    back_translated_sentence='not translated',
                    evaluation=default_evaluation
                )
                for language in target_languages
            }
            for sentence_id, original_sentence in sentences.items()
        }

    def update(self, sentence_id: str, language: str, new_back_translation: BackTranslationEvaluation):
        """Обновление обратного перевода для конкретного языка"""
        if self.target_languages is None:
            raise RuntimeError("Handler not initialized. Call initialize() first.")
        if sentence_id not in self.back_translations:
            raise KeyError(f"ID {sentence_id} не найден")
        if language not in self.target_languages:
            raise ValueError(f"Язык {language} не поддерживается. Доступные: {self.target_languages}")

        try:
            self.back_translations[sentence_id][language].back_translated_sentence = new_back_translation.back_translated_sentence
            self.back_translations[sentence_id][language].evaluation = new_back_translation.evaluation
        except ValueError:
            raise ValueError(
                f"Недопустимый обратный перевод: {new_back_translation}."
            )

    def get_original_sentence(self, sentence_id: str) -> str:
        return self.back_translations[sentence_id][self.target_languages[0]].original_sentence

    def get_list_back_translation(self) -> List[BackTranslationEvaluations]:
        """Получение всех обратных переводов в виде списка"""
        if self.target_languages is None:
            raise RuntimeError("Handler not initialized. Call initialize() first.")

        evaluations_list = []

        for sentence_id, language_dict in self.back_translations.items():
            for language_code, evaluation_data in language_dict.items():
                evaluation = BackTranslationEvaluations(
                    sentence_id=sentence_id,
                    language_code=language_code,
                    original_sentence=evaluation_data.original_sentence,
                    back_translated_sentence=evaluation_data.back_translated_sentence,
                    evaluation=evaluation_data.evaluation
                )
                evaluations_list.append(evaluation)

        return evaluations_list

    def get_map_back_translations(self) -> Dict[str, Dict[str, BackTranslationEvaluation]]:
        """Получение всех обратных переводов в виде словаря"""
        return self.back_translations


back_translation_evaluations = BackTranslationEvaluationHandler()
