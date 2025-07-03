from pydantic import BaseModel

from app.schemas.sentences.sentence_detail_base import SentenceDetailBase
from app.schemas.sentences.sentence_detail_translated import SentenceDetailTranslated


class Sentence(BaseModel):
    id: int
    original_sentence: SentenceDetailBase
    translated_sentence: list[SentenceDetailTranslated]
