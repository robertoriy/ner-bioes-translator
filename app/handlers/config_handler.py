from typing import Optional

from app.schemas.config.service_config import ServiceConfig


class ConfigHandler:
    def __init__(self):
        self._config: Optional[ServiceConfig] = None

    def save_config(self, config: ServiceConfig) -> ServiceConfig:
        self._config = config
        return self._config

    def get_config(self) -> ServiceConfig:
        if self._config is None:
            raise ValueError("Config еще не загружен")
        return self._config

config_handler = ConfigHandler()