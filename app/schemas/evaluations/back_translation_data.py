from pydantic import BaseModel


class BackTranslationData(BaseModel):
    language_code: str
    back_translated_sentence: str
    evaluation: float