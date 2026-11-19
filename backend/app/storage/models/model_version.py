from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.storage.models.shot import Shot


class ModelVersion(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "model_versions"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "version",
            name="uq_model_versions_name_version",
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    framework: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    format: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    artifact_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    training_params: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    validation_metrics: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    trained_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    shots: Mapped[list["Shot"]] = relationship(
        back_populates="model_version",
    )