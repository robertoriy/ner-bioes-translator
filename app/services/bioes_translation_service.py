from openai import OpenAI

from app.schemas.config.service_config import ServiceConfig
from config import settings


class BioesTranslationService:
    def __init__(self):
        self._client = OpenAI(
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
        )

    def translate(self, sentence_bioes: str, language: str, config: ServiceConfig):
        prompt_config = config.prompt_data
        task = prompt_config.task
        role, answer = prompt_config.get_bioes_role_and_answer(language)

        print("\n-----------------")
        print(f"Обработка запроса на перевод с сохранением разметки:\n"
              f"role - {role} | \n"
              f"example task - {task} | \n"
              f"answer - {answer}| \n"
              f"sentence to translate - {sentence_bioes}")

        chat_completion = self._client.chat.completions.create(
            model=config.model,
            messages=[
                {
                    "role": "system",
                    "content": role
                },
                {
                    "role": "user",
                    "content": task
                },
                {
                    "role": "assistant",
                    "content": answer
                },
                {
                    "role": "user",
                    "content": sentence_bioes
                }
            ],
            temperature=0.3
        )
        print(chat_completion)
        result = chat_completion.choices[0].message.content

        print(f"Результат обработки запроса на перевод с сохранением разметки:\n"
              f"result - {result}")
        print("-----------------\n")

        return result


bioes_translator = BioesTranslationService()
