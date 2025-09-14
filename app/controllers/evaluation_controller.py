from fastapi import APIRouter, HTTPException

from app.dependencies.dependencies import get_expert_evaluations, get_back_translator, \
    get_config_handler, get_result_df_handler
from app.handlers.back_translation_evaluation_handler import back_translation_evaluations
from app.schemas.evaluations.back_translation_evaluations import BackTranslationEvaluations
from app.schemas.evaluations.expert_evaluation import ExpertEvaluation
from app.schemas.evaluations.expert_evaluations import ExpertEvaluations
from app.schemas.evaluations.statistics import Statistics

evaluation_router = APIRouter(
    prefix="/api/v1",
    tags=["Evaluation operations"]
)


@evaluation_router.get("/evaluations/expert")
async def get_expert_evaluations_data() -> Statistics:
    try:
        return get_expert_evaluations().calculate_statistics()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": str(e),
                "hint": "Не получилось посчитать статистику"
            }
        )


@evaluation_router.post("/evaluations/expert/{sentence_id}")
async def update_expert_evaluation(
        sentence_id: int,
        new_evaluation: ExpertEvaluation
) -> list[ExpertEvaluations]:
    try:
        expert_evaluations = get_expert_evaluations()
        expert_evaluations.update(str(sentence_id), new_evaluation.language_code, new_evaluation.evaluation)
        return expert_evaluations.get_list_evaluations()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": str(e),
                "hint": "Не получилось обновить оценку"
            }
        )


@evaluation_router.get("/evaluations/back_translations")
async def get_back_translation_evaluations_data() -> list[BackTranslationEvaluations]:
    try:
        return back_translation_evaluations.get_list_back_translation()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": str(e),
                "hint": "Не получилось получить статистику"
            }
        )


@evaluation_router.post("/evaluations/back_translations")
async def do_back_translation_evaluations():
    try:
        df = get_result_df_handler().get_dataframe().copy(deep=True)
        config = get_config_handler().get_config()

        back_translator = get_back_translator()
        return back_translator.make_evaluation(df, config)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "error": e,
                "message": str(e),
                "hint": "Не получилось обновить оценку"
            }
        )
