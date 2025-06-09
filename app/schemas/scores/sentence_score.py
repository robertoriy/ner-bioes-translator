from pydantic import BaseModel

class SentenceScore(BaseModel):
    language_code: str
    evaluation_score: str