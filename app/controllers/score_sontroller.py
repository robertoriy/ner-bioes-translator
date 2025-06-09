from fastapi import APIRouter, HTTPException

from app.dependencies.dependencies import get_sentence_scores
from app.schemas.scores.sentence_score import SentenceScore

score_router = APIRouter(
    prefix="/api/v1",
    tags=["Score operations"]
)

@score_router.get("/scores")
async def get_scores():
    try:
        return get_sentence_scores().calculate_statistics()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": str(e),
                "hint": "Не получилось посчитать статистику"
            }
        )

@score_router.post("/scores/{sentence_id}")
async def update_scores(
        sentence_id: int,
        new_score: SentenceScore
):
    try:
        scores = get_sentence_scores()
        scores.update(str(sentence_id), new_score.language_code, new_score.evaluation_score)
        return scores.get_as_evaluations()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": str(e),
                "hint": "Не получилось обновить оценку"
            }
        )
