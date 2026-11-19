from fastapi import FastAPI, HTTPException

from app.config import settings
from app.storage.database import check_database_connection


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI shooting target analyzer API",
)


@app.get("/api/v1/health", tags=["System"])
def health():
    """
    Проверка состояния приложения и подключения к базе данных.
    """
    database_available = check_database_connection()

    if not database_available:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "unavailable",
            },
        )

    return {
        "status": "ok",
        "database": "connected",
    }