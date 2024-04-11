from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="RANDOM_GENERATOR_FRONTEND_",
        env_file_encoding="utf-8",
    )

    backend_url: str = "http://localhost:8000"


settings = Settings()
