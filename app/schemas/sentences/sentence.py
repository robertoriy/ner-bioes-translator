from pydantic import BaseModel

from app.schemas.sentences.sentence_detail import SentenceDetail


class Sentence(BaseModel):
    id: int
    original_sentence: SentenceDetail
    translated_sentence: list[SentenceDetail]