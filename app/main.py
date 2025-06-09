from fastapi import FastAPI, Depends
from app.controllers.config_controller import config_router
from app.controllers.data_controller import data_router
from app.controllers.score_sontroller import score_router
from app.controllers.upload_controller import upload_router
from app.dependencies.dependencies import get_df_handler
from app.services.df_handler import DataFrameHandler

app = FastAPI()

app.include_router(config_router)
app.include_router(upload_router)
app.include_router(data_router)
app.include_router(score_router)

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }


@app.get("/hello")
async def say_hello(
        handler: DataFrameHandler = Depends(get_df_handler)
):
    return handler.get_dataframe().head(2).to_json(orient='records')
