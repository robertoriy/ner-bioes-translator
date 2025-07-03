from collections import defaultdict
from typing import Dict, List, Optional

from app.schemas.evaluations.expert_evaluations import ExpertEvaluations
from app.schemas.evaluations.language_statistics import LanguageStatistics
from app.schemas.evaluations.expert_evaluation_values import ExpertEvaluationValues
from app.schemas.evaluations.statistics import Statistics


class ExpertEvaluationHandler:
    def __init__(self):
        self._expert_evaluations: Dict[str, Dict[str, ExpertEvaluationValues]] = {}  # {sentence_id: {language: score}}
        self.target_languages: Optional[List[str]] = None

    def initialize(
            self,
            ids: Dict[str, str],
            target_languages: List[str],
            default_score: ExpertEvaluationValues = ExpertEvaluationValues.NOT_EVALUATED
    ):
        """Инициализация с дефолтными значениями для всех языков"""
        self.target_languages = target_languages
        self._expert_evaluations = {
            sentence_id.split()[1]: {lang: default_score for lang in target_languages}
            for sentence_id in ids
        }

    def update(self, sentence_id: str, language: str, new_evaluation: str):
        """Обновление оценки для конкретного языка"""
        if self.target_languages is None:
            raise RuntimeError("Handler not initialized. Call initialize() first.")
        if sentence_id not in self._expert_evaluations:
            raise KeyError(f"ID {sentence_id} не найден")
        if language not in self.target_languages:
            raise ValueError(f"Язык {language} не поддерживается. Доступные: {self.target_languages}")

        try:
            validated_score = ExpertEvaluationValues(new_evaluation.lower())
            self._expert_evaluations[sentence_id][language] = validated_score
        except ValueError:
            raise ValueError(
                f"Недопустимая оценка: {new_evaluation}. "
                f"Допустимые значения: {[e.value for e in ExpertEvaluationValues]}"
            )

    def get_list_evaluations(self) -> List[ExpertEvaluations]:
        """Получение всех оценок в виде списка"""
        if self.target_languages is None:
            raise RuntimeError("Handler not initialized. Call initialize() first.")

        return [
            ExpertEvaluations(
                sentence_id=sentence_id,
                language_code=lang,
                evaluation=evaluation.value
            )
            for sentence_id, expert_evaluation in self._expert_evaluations.items()
            for lang, evaluation in expert_evaluation.items()
        ]

    def get_map_evaluations(self) -> Dict[str, Dict[str, ExpertEvaluationValues]]:
        """Получение всех оценок в виде словаря"""
        return self._expert_evaluations

    def calculate_statistics(self) -> Statistics:
        if self.target_languages is None:
            raise RuntimeError("Handler not initialized. Call initialize() first.")

        total_sentences = 0
        correct_sentences = 0
        incorrect_sentences = 0
        not_evaluated_sentences = 0

        language_stats = defaultdict(lambda: {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "not_evaluated": 0,
        })

        for sentence_id, lang_scores in self._expert_evaluations.items():
            for lang, score in lang_scores.items():
                total_sentences += 1
                language_stats[lang]["total"] += 1

                if score == ExpertEvaluationValues.CORRECT:
                    correct_sentences += 1
                    language_stats[lang]["correct"] += 1
                elif score == ExpertEvaluationValues.INCORRECT:
                    incorrect_sentences += 1
                    language_stats[lang]["incorrect"] += 1
                else:  # NOT_EVALUATED
                    not_evaluated_sentences += 1
                    language_stats[lang]["not_evaluated"] += 1

        language_statistics = [
            LanguageStatistics(
                language_code=lang,
                total_sentences=stats["total"],
                correct_sentences=stats["correct"],
                incorrect_sentences=stats["incorrect"],
                not_evaluated_sentences=stats["not_evaluated"],
            )
            for lang, stats in language_stats.items()
        ]

        return Statistics(
            total_sentences=total_sentences,
            correct_sentences=correct_sentences,
            incorrect_sentences=incorrect_sentences,
            not_evaluated_sentences=not_evaluated_sentences,
            language_statistics=language_statistics,
        )


expert_evaluations = ExpertEvaluationHandler()
