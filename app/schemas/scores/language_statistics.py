from pydantic import BaseModel


class LanguageStatistics(BaseModel):
    language_code: str
    total_sentences: int
    correct_sentences: int
    incorrect_sentences: int
    not_evaluated_sentences: int