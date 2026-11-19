
import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import (
    DateTime,
    MetaData,
    Uuid,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


# Единая схема именования ограничений и индексов.
# Это упрощает работу Alembic и сопровождение миграций.
NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """
    Базовый класс всех SQLAlchemy-моделей проекта.

    Содержит общую metadata с едиными правилами
    именования объектов базы данных.
    """

    metadata = MetaData(
        naming_convention=NAMING_CONVENTION,
    )


class UUIDPrimaryKeyMixin:
    """
    Примесь для моделей с UUID в качестве первичного ключа.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class CreatedAtMixin:
    """
    Примесь для моделей, которым необходимо хранить
    время создания записи.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class TimestampMixin(CreatedAtMixin):
    """
    Примесь для моделей, которым необходимо хранить
    время создания и последнего обновления.
    """

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
