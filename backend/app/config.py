import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY", "super_secret_dev_key")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./siddque_ai.db")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()