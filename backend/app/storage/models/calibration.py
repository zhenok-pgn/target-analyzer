from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.storage.models.calibration_point import CalibrationPoint
    from app.storage.models.shooting_session import ShootingSession
    from app.storage.models.shot import Shot


class Calibration(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "calibrations"

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "version",
            name="uq_calibrations_session_version",
        ),
        CheckConstraint(
            "version >= 1",
            name="ck_calibrations_version_positive",
        ),
        CheckConstraint(
            "mm_per_pixel > 0",
            name="ck_calibrations_mm_per_pixel_positive",
        ),
        CheckConstraint(
            "calibration_error >= 0",
            name="ck_calibrations_error_non_negative",
        ),
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("shooting_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    h11: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h12: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h13: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h21: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h22: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h23: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h31: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h32: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )
    h33: Mapped[Decimal] = mapped_column(
        Numeric(18, 12),
        nullable=False,
    )

    mm_per_pixel: Mapped[Decimal] = mapped_column(
        Numeric(12, 8),
        nullable=False,
    )

    calibration_error: Mapped[Decimal] = mapped_column(
        Numeric(12, 6),
        nullable=False,
    )

    session: Mapped["ShootingSession"] = relationship(
        back_populates="calibrations",
    )

    points: Mapped[list["CalibrationPoint"]] = relationship(
        back_populates="calibration",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    shots: Mapped[list["Shot"]] = relationship(
        back_populates="calibration",
    )