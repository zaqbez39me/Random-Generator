import enum
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for seed fetchers
    news_api_key: str
    news_query: str = "tesla"
    weather_latitude: float = 55.752116
    weather_longitude: float = 48.744554
    requests_timeout: float = 3.0
    time_zone: str = "Europe/Amsterdam"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RANDOM_GENERATOR_",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
