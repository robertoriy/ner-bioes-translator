from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

from app.dependencies.dependencies import get_df_handler

upload_router = APIRouter(
    prefix="/api/v1",
    tags=["Upload operations"]
)

@upload_router.post("/dataset/excel")
async def upload_dataset_excel(
        file: UploadFile = File(...)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, detail="Invalid file format. Please upload an Excel file.")

    df_handler = get_df_handler()
    try:
        contents = await file.read()
        df = pd.read_excel(
            BytesIO(contents),
            usecols=['Sentence', 'Word', 'BIOES-Tag'],
            engine='openpyxl'
        )
        df_handler.set_dataframe(df)

        result = df.head(2).to_dict(orient="records")

        return {
            "filename": file.filename,
            "data": result
        }
    except Exception as e:
        raise HTTPException(500, detail=f"Error processing file: {str(e)}")