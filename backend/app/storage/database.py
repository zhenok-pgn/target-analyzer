from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config import settings


engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def check_database_connection() -> bool:
    """
    Проверяет доступность PostgreSQL.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False