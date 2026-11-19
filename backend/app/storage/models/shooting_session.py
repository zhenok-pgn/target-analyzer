from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime

from app.storage.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from app.storage.models.calibration import Calibration
    from app.storage.models.media_asset import MediaAsset
    from app.storage.models.metrics_snapshot import MetricsSnapshot
    from app.storage.models.series import Series
    from app.storage.models.target_profile_version import TargetProfileVersion
    from app.storage.models.user import User


class ShootingSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "shooting_sessions"

    __table_args__ = (
        CheckConstraint(
            "source_type IN ('browser', 'file', 'image', 'scan', 'rtsp')",
            name="source_type_valid",
        ),
        CheckConstraint(
            "status IN ('created', 'processing', 'completed', 'failed', 'archived')",
            name="status_valid",
        ),
        CheckConstraint(
            "caliber_mm IS NULL OR caliber_mm > 0",
            name="caliber_positive",
        ),
        CheckConstraint(
            "distance_m IS NULL OR distance_m > 0",
            name="distance_positive",
        ),
        CheckConstraint(
            "revision >= 0",
            name="revision_non_negative",
        ),
        Index("ix_shooting_sessions_user_id", "user_id"),
        Index("ix_shooting_sessions_profile_version_id", "profile_version_id"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    profile_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("target_profile_versions.id", ondelete="RESTRICT"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    source_params: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    weapon_description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    caliber_mm: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 3),
        nullable=True,
    )

    distance_m: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    conditions: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="created",
        server_default=text("'created'"),
    )

    started_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
)

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revision: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    user: Mapped["User"] = relationship(
        back_populates="shooting_sessions",
    )

    profile_version: Mapped["TargetProfileVersion"] = relationship(
        back_populates="shooting_sessions",
    )

    series: Mapped[list["Series"]] = relationship(
        back_populates="session",
    )

    calibrations: Mapped[list["Calibration"]] = relationship(
        back_populates="session",
    )

    media_assets: Mapped[list["MediaAsset"]] = relationship(
        back_populates="session",
    )

    metrics_snapshots: Mapped[list["MetricsSnapshot"]] = relationship(
        back_populates="session",
    )