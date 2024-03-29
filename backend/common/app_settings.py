import os
import time
from typing import Optional, List, Dict, Any

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
    REDIS_MAX_CONNECTIONS: int = 10
    SENTRY_DSN: str
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    SESSION_COOKIE_NAME: str
    SESSION_SECRET_KEY: str
    GOOGLE_API_CLIENT_ID: str
    LOGGER_SINK: str = f"file_{time.time()}.log"
    LOGGER_ROTATION_MEM_LIMIT: str
    LOGGER_RETENTION_DAYS: str
    LOGGER_LOG_LEVEL: str
    LOGGER_COMPRESSION: str = "zip"
    LOGGER_ENQUEUE: bool = True
    LOGGER_BACKTRACE: bool = False
    LOGGER_SERIALIZE: bool = True
    DEFAULT_ES_INDEX_SETTINGS: Dict[Any, Any] = {"number_of_shards": 3, "number_of_replicas": 2}

    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_HOST: str = "localhost"
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
