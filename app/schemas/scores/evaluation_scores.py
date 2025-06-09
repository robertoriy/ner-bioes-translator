from pydantic import BaseModel


class EvaluationScores(BaseModel):
    sentence_id: str
    language_code: str
    evaluation_score: str