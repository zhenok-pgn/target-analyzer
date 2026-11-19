from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.models.base import Base, UUIDPrimaryKeyMixin


class DatasetSource(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "dataset_sources"

    __table_args__ = (
        CheckConstraint(
            "image_count >= 0",
            name="ck_dataset_sources_image_count_non_negative",
        ),
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    license: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    image_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    annotation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    dataset_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )