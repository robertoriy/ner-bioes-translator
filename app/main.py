from fastapi import FastAPI
from app.controllers.config_controller import config_router
from app.controllers.data_controller import data_router
from app.controllers.evaluation_controller import evaluation_router
from app.controllers.upload_controller import upload_router

app = FastAPI()

app.include_router(config_router)
app.include_router(upload_router)
app.include_router(data_router)
app.include_router(evaluation_router)

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }
