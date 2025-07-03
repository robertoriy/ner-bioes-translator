from pydantic import BaseModel

class ExpertEvaluation(BaseModel):
    language_code: str
    evaluation: str