import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class EnvironmentSettings(BaseSettings):
    """
    Manages application settings by loading from environment variables.
    """

    # Application Settings
    LOG_LEVEL: str = "INFO"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    # Redis Settings
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_CONTEXT_ENGINE_DB: int
    REDIS_USER_NAME: str
    REDIS_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


try:
    settings = EnvironmentSettings()
except Exception as e:
    logger.error(f"FATAL: Could not load application settings. Error: {e}")
    settings = None
