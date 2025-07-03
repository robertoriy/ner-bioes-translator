from pydantic import BaseModel

class BackTranslationPrompt(BaseModel):
    role: str
    task: str