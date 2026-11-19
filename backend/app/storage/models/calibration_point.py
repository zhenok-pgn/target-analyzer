from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.storage.models.calibration import Calibration


class CalibrationPoint(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "calibration_points"

    __table_args__ = (
        UniqueConstraint(
            "calibration_id",
            "point_number",
            name="uq_calibration_points_calibration_point_number",
        ),
        CheckConstraint(
            "point_number BETWEEN 1 AND 4",
            name="ck_calibration_points_point_number_range",
        ),
    )

    calibration_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("calibrations.id", ondelete="CASCADE"),
        nullable=False,
    )

    point_number: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    pixel_x: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    pixel_y: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    calibration: Mapped["Calibration"] = relationship(
        back_populates="points",
    )