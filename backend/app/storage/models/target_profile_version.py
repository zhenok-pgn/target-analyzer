from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import (
    Base,
    CreatedAtMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from app.storage.models.shooting_session import ShootingSession
    from app.storage.models.target_profile import TargetProfile
    from app.storage.models.target_zone import TargetZone


class TargetProfileVersion(
    UUIDPrimaryKeyMixin,
    CreatedAtMixin,
    Base,
):
    __tablename__ = "target_profile_versions"

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "version",
            name="uq_target_profile_versions_profile_version",
        ),
        CheckConstraint(
            "version >= 1",
            name="version_positive",
        ),
        CheckConstraint(
            "sheet_width_mm > 0",
            name="sheet_width_positive",
        ),
        CheckConstraint(
            "sheet_height_mm > 0",
            name="sheet_height_positive",
        ),
        CheckConstraint(
            "scoring_mode IN ('integer', 'decimal')",
            name="scoring_mode_valid",
        ),
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("target_profiles.id", ondelete="RESTRICT"),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    sheet_width_mm: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    sheet_height_mm: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    aim_x_mm: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    aim_y_mm: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    scoring_mode: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    account_caliber: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    coordinate_system: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    reference_image_path: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    profile: Mapped["TargetProfile"] = relationship(
        back_populates="versions",
    )

    zones: Mapped[list["TargetZone"]] = relationship(
        back_populates="profile_version",
    )

    shooting_sessions: Mapped[list["ShootingSession"]] = relationship(
        back_populates="profile_version",
    )