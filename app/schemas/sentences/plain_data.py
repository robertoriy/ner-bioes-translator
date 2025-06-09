from pydantic import BaseModel

from app.schemas.sentences.bioes_tag import BioesTag


class PlainData(BaseModel):
    word: str
    tag: BioesTag