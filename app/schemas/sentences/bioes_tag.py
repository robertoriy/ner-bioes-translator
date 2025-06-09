from pydantic import BaseModel

class BioesTag(BaseModel):
    full_tag: str
    prefix: str
    type: str