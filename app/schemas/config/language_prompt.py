from pydantic import BaseModel

from app.schemas.config.back_translation_prompt import BackTranslationPrompt
from app.schemas.config.bioes_prompt import BioesPrompt
from app.schemas.config.language import Language


class LanguagePrompt(BaseModel):
    language: Language
    bioes_prompt: BioesPrompt
    back_translation_prompt: BackTranslationPrompt