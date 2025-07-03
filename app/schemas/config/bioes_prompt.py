from pydantic import BaseModel


class BioesPrompt(BaseModel):
    role: str
    answer: str