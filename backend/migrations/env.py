
from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Добавляем backend в Python path, чтобы Alembic мог импортировать app.
BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.storage.models import Base  # noqa: E402
from dotenv import load_dotenv


# Конфигурация Alembic.
config = context.config

# Настраиваем логирование из alembic.ini, если файл конфигурации указан.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Получаем URL базы данных из переменной окружения.
# Если DATABASE_URL не задана, используется sqlalchemy.url из alembic.ini.
load_dotenv(BACKEND_DIR.parent / ".env")
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Экранируем символ %, поскольку Config использует configparser.
    config.set_main_option(
        "sqlalchemy.url",
        database_url.replace("%", "%%"),
    )

# Метаданные всех моделей приложения.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций без создания подключения к базе данных.

    SQL миграций формируется на основе URL и метаданных моделей.
    """
    url = config.get_main_option("sqlalchemy.url")

    if not url:
        raise RuntimeError(
            "Не задан URL базы данных. "
            "Укажите DATABASE_URL или sqlalchemy.url в alembic.ini."
        )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Запуск миграций с подключением к базе данных.
    """
    configuration = config.get_section(config.config_ini_section)

    if configuration is None:
        raise RuntimeError(
            "Не удалось прочитать секцию конфигурации Alembic."
        )

    configuration["sqlalchemy.url"] = config.get_main_option(
        "sqlalchemy.url"
    )

    if not configuration["sqlalchemy.url"]:
        raise RuntimeError(
            "Не задан URL базы данных. "
            "Укажите DATABASE_URL или sqlalchemy.url в alembic.ini."
        )

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                compare_server_default=True,
                include_schemas=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
