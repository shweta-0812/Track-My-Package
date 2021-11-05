import os
from typing import Optional, List

from pydantic import BaseSettings, AnyHttpUrl

env_file_name: Optional[str]

if os.environ.get("IS_PRODUCTION") == "True":
    env_file_name = None
else:
    env_file_name = "backend/.env"

BASE_DIR: str = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
ENV_FILE: Optional[str] = os.path.join(
    BASE_DIR, env_file_name
) if env_file_name else None


class Settings(BaseSettings):
    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"

    PROJECT_NAME: str
    IS_PRODUCTION: bool
    APP_SERVER_URL: str
    ES_DATABASE_URL: str
    REDIS_URL: str
    SESSION_COOKIE_NAME: str
    SESSION_SECRET_KEY: str
    GOOGLE_API_CLIENT_ID: str
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://localhost",
        "https://localhost:4200",
        "https://localhost:3000",
        "https://localhost:8080",
        "http://dev.flydata.com",
        "https://stag.flydata.com",
        "https://flydata.com",
    ]


app_settings: Settings = Settings()
