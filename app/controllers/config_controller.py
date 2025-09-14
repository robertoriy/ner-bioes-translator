from fastapi import APIRouter, HTTPException
from app.dependencies.dependencies import get_config_handler
from app.schemas.config.service_config import ServiceConfig

config_router = APIRouter(
    prefix="/api/v1",
    tags=["Config operations"]
)

@config_router.get("/config")
async def get_current_config() -> ServiceConfig:
    config_handler = get_config_handler()
    try:
        current_config = config_handler.get_config()
        return current_config
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": str(e),
                "hint": "Config ещё не загружен"
            }
        )

@config_router.post("/config")
async def save_new_config(config: ServiceConfig) -> ServiceConfig:
    config_handler = get_config_handler()
    saved_config = config_handler.save_config(config)
    return saved_config