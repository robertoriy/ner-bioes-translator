from typing import Optional

from pydantic import BaseModel

from app.schemas.config.language import Language
from app.schemas.sentences.plain_data import PlainData


class SentenceDetail(BaseModel):
    language: Language
    full_sentence: str
    named_entity: list[str]
    content: list[PlainData]
    evaluation_score: Optional[str] = None

    class Config:
        exclude_unset = True