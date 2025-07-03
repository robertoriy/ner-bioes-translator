from openai import OpenAI

from config import settings


class OpenAiClientHandler:
    def __init__(self):
        self._client = OpenAI(
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
        )

    def get_client(self) -> OpenAI:
        if self._client is None:
            raise ValueError("OpenAI client еще не создан")
        return self._client