from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Query
from starlette.responses import StreamingResponse

from app.dependencies.dependencies import get_df_handler, get_config_handler, \
    get_result_df_handler, get_expert_evaluations
from app.handlers.back_translation_evaluation_handler import back_translation_evaluations
from app.schemas.evaluations.expert_evaluation_values import ExpertEvaluationValues
from app.utils.df_mapper import DataFrameMapper
from app.utils.df_processor import DataFrameProcessor

data_router = APIRouter(
    prefix="/api/v1",
    tags=["Data operations"]
)


@data_router.get("/dataset/excel")
async def download_excel():
    df = get_result_df_handler().get_dataframe().copy(deep=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')

    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="report.xlsx"',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }

    return StreamingResponse(output, headers=headers)


@data_router.get("/dataset")
async def get_all_sentences_short():
    df = get_result_df_handler().get_dataframe().copy(deep=True)
    expert_evaluations = get_expert_evaluations().get_map_evaluations()
    return DataFrameMapper.df_to_sentences_json(
        df,
        expert_evaluations,
        back_translation_evaluations.get_map_back_translations()
    )


@data_router.get("/dataset/{sentence_id}")
async def get_special_sentence(sentence_id: int):
    df = get_result_df_handler().get_dataframe().copy(deep=True)
    expert_evaluations = get_expert_evaluations().get_map_evaluations()
    return DataFrameMapper.df_to_sentence_json(
        df,
        sentence_id,
        expert_evaluations,
        back_translation_evaluations.get_map_back_translations()
    )


@data_router.post("/dataset/translation")
async def get_translations(
        language: list[str] = Query(..., description="Список языков в формате ISO 639-1 (например, ru,en,kk)"),
        from_sentence: int = Query(..., description="С какого предлоежния производить перевод"),
        to_sentence: int = Query(..., description="До какого предложения производить перевод")
):
    print("params - " + str(language) + " " + str(from_sentence) + " " + str(to_sentence))
    if from_sentence >= to_sentence:
        return {
            "message": "Переданы некорректные параметры для начального и конечного предложения"
        }

    df = get_df_handler().get_dataframe().copy(deep=True)

    config_language = get_config_handler().get_config().prompt_data.get_languages()
    target_languages = list(set(language) & set(config_language))

    print("Будут использоваться переводы на - " + str(target_languages))

    unique_sentences = df['Sentence'].unique()[from_sentence:to_sentence]
    original_sentences = {
        sentence: ' '.join(df[df['Sentence'] == sentence]['Word'])
        for sentence in unique_sentences
    }

    expert_evaluations = get_expert_evaluations()
    expert_evaluations.initialize(
        unique_sentences,
        target_languages,
        ExpertEvaluationValues.NOT_EVALUATED
    )

    back_translation_evaluations.initialize(
        original_sentences,
        target_languages,
        0.0
    )

    print("Отрезали лишние предложения")
    sentence_data = {
        sentence_name: df[df['Sentence'] == sentence_name]
        for sentence_name in unique_sentences
    }

    print("Делаем запрос на перевод")
    translations = DataFrameProcessor.get_translations(sentence_data, target_languages)
    print("Получили перевод. Обновляем DF")
    new_df = DataFrameProcessor.update_df(df, unique_sentences, translations)
    result_df_handler = get_result_df_handler()
    result_df_handler.set_dataframe(new_df)

    print("DF обновлен")

    return {
        "message": "Задача обработана"
    }
