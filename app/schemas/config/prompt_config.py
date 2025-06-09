from pydantic import BaseModel

from app.schemas.config.language import Language
from app.schemas.config.language_prompt import LanguagePrompt

class LanguageNotFoundError(Exception):
    pass

class PromptConfig(BaseModel):
    task: str
    source_language: Language
    target_data: list[LanguagePrompt]

    def get_original_language(self):
        return self.source_language.code

    def get_extended_original_language(self):
        return self.source_language

    def get_languages(self):
        languages = []
        for target in self.target_data:
            languages.append(target.language.code)
        return languages

    def get_extended_languages(self):
        languages = []
        for target in self.target_data:
            languages.append(target.language)
        return languages

    def get_extended_language(self, code: str):
        for target in self.target_data:
            if target.language.code == code:
                return target.language
        raise LanguageNotFoundError

    def get_role_and_answer(self, language_code: str) -> tuple[str, str]:
        """Возвращает (role, answer) или вызывает исключение, если language_code не найден."""
        target_data = None
        for target in self.target_data:
            if target.language.code == language_code:
                target_data = target
        if not target_data:
            raise LanguageNotFoundError(f"Language code '{language_code}' not found in config")
        return target_data.role, target_data.answer