import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = os.getenv("APP_ENV", "dev")

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    SECRET_KEY: str = "super_secret_jwt_key_hs256_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(
        env_file=f".env.{env_state}",
        extra="ignore"
    )

settings = Settings()