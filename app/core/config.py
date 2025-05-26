# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "KYC Backend"
    VERSION: str = "1.0.0"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_HOST: str
    REDIS_PORT: int
    MAX_FILE_SIZE: int
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()
