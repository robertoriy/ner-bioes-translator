from pydantic import BaseModel

from app.schemas.evaluations.back_translation_data import BackTranslationData
from app.schemas.evaluations.expert_evaluation import ExpertEvaluation


class SentenceShort(BaseModel):
    id: int
    original_sentence: str
    expert_evaluation: list[ExpertEvaluation]
    back_translation_evaluation: list[BackTranslationData]