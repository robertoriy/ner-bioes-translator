from pydantic import BaseModel

from app.schemas.config.language import Language


class LanguagePrompt(BaseModel):
    language: Language
    role: str
    answer: str