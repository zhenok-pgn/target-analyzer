from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import (
    Base,
    UUIDPrimaryKeyMixin,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.storage.models.target_profile_version import TargetProfileVersion

class TargetZone(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "target_zones"

    __table_args__ = (
        CheckConstraint(
            "geometry_type IN "
            "('circle', 'annulus', 'rectangle', 'polygon', 'arc')",
            name="geometry_type_valid",
        ),
    )

    profile_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "target_profile_versions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    geometry_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    geometry: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    score_value: Mapped[Decimal] = mapped_column(
        Numeric(8, 3),
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    profile_version: Mapped["TargetProfileVersion"] = relationship(
        back_populates="zones",
    )