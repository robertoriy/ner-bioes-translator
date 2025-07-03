from pydantic import BaseModel


class BackTranslationEvaluations(BaseModel):
    sentence_id: str
    language_code: str
    original_sentence: str
    back_translated_sentence: str
    evaluation: float