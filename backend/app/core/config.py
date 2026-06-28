from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "GeoVision AI"
    environment: str = "development"
    secret_key: str = "dev-only-change-in-prod"
    database_url: str = "postgresql://geovision:geovision123@localhost:5432/geovision_db"
    backend_cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()