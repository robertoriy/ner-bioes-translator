from pydantic import BaseModel

from app.schemas.config.language import Language
from app.schemas.sentences.plain_data import PlainData


class SentenceDetailBase(BaseModel):
    language: Language
    full_sentence: str
    named_entity: list[str]
    content: list[PlainData]
