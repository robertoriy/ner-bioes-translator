from typing import Optional

from pydantic import BaseModel

from app.schemas.config.language import Language
from app.schemas.evaluations.back_translation_evaluation import BackTranslationEvaluation
from app.schemas.sentences.plain_data import PlainData


class SentenceDetailTranslated(BaseModel):
    language: Language
    full_sentence: str
    named_entity: list[str]
    content: list[PlainData]
    expert_evaluation: Optional[str] = None
    back_translation_evaluation: Optional[BackTranslationEvaluation] = None