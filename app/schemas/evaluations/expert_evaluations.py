from pydantic import BaseModel


class ExpertEvaluations(BaseModel):
    sentence_id: str
    language_code: str
    evaluation: str