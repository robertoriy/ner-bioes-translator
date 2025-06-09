from pydantic import BaseModel

from app.schemas.scores.language_statistics import LanguageStatistics


class Statistics(BaseModel):
    total_sentences: int
    correct_sentences: int
    incorrect_sentences: int
    not_evaluated_sentences: int
    language_statistics: list[LanguageStatistics]