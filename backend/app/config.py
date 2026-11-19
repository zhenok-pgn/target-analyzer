import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = "Target Analyzer"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://target:change_this_password@localhost:5432/target",
    )


settings = Settings()