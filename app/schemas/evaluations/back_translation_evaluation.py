from pydantic import BaseModel


class BackTranslationEvaluation(BaseModel):
    original_sentence: str
    back_translated_sentence: str
    evaluation: float