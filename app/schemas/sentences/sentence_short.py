from pydantic import BaseModel

from app.schemas.scores.sentence_score import SentenceScore


class SentenceShort(BaseModel):
    id: int
    original_sentence: str
    evaluation_score: list[SentenceScore]