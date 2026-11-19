from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.storage.models.calibration import Calibration
    from app.storage.models.media_asset import MediaAsset
    from app.storage.models.model_version import ModelVersion
    from app.storage.models.series import Series
    from app.storage.models.shot_revision import ShotRevision


class Shot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "shots"

    __table_args__ = (
        UniqueConstraint(
            "series_id",
            "shot_number",
            name="uq_shots_series_shot_number",
        ),
        CheckConstraint(
            "shot_number >= 1",
            name="ck_shots_shot_number_positive",
        ),
        CheckConstraint(
            "confidence IS NULL OR confidence BETWEEN 0 AND 1",
            name="ck_shots_confidence_range",
        ),
        CheckConstraint(
            "hole_diameter_mm IS NULL OR hole_diameter_mm > 0",
            name="ck_shots_hole_diameter_positive",
        ),
        CheckConstraint(
            "shot_time_ms IS NULL OR shot_time_ms >= 0",
            name="ck_shots_time_non_negative",
        ),
        CheckConstraint(
            "source_type IN ('automatic', 'manual')",
            name="ck_shots_source_type",
        ),
        CheckConstraint(
            "status IN ('active', 'false')",
            name="ck_shots_status",
        ),
    )

    series_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("series.id"),
        nullable=False,
        index=True,
    )

    calibration_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("calibrations.id"),
        nullable=True,
        index=True,
    )

    model_version_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("model_versions.id"),
        nullable=True,
        index=True,
    )

    media_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id"),
        nullable=True,
        index=True,
    )

    shot_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    x_mm: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    y_mm: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    shot_time_ms: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    confidence: Mapped[Decimal | None] = mapped_column(
        Numeric(6, 5),
        nullable=True,
    )

    hole_diameter_mm: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 3),
        nullable=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        server_default="active",
    )

    is_double_hit: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    series: Mapped["Series"] = relationship(
        back_populates="shots",
    )

    calibration: Mapped["Calibration | None"] = relationship(
        back_populates="shots",
    )

    model_version: Mapped["ModelVersion | None"] = relationship(
        back_populates="shots",
    )

    media_asset: Mapped["MediaAsset | None"] = relationship(
        back_populates="shots",
    )

    revisions: Mapped[list["ShotRevision"]] = relationship(
        back_populates="shot",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ShotRevision.revision_number",
    )