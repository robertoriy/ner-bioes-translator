from pydantic import BaseModel

from app.schemas.config.prompt_config import PromptConfig


class ServiceConfig(BaseModel):
    model: str
    prompt_data: PromptConfig