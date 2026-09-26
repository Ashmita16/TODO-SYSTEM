import os
from pydantic_settings import BaseSettings

env_state = os.getenv("APP_ENV", "dev")
env_file = f".env.{env_state}"

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    SECRET_KEY: str = "super_secret_jwt_key_hs256_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = env_file
        extra = "ignore"

settings = Settings()