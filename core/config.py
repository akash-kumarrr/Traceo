from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name : str = "traceo-backend"
    app_version : str = "1.0.0"
    app_description : str = "backend system of traceo application"

    db_url : str
    redis_url : str

    app_secret_key : str
    access_token_expire_minutes : int
    algorithm : str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # ignores extra environment variables without throwing errors
    )

settings = Settings()