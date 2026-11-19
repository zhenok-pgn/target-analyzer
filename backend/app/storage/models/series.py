from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from app.storage.models.metrics_snapshot import MetricsSnapshot
    from app.storage.models.shot import Shot
    from app.storage.models.shooting_session import ShootingSession


class Series(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "series"

    __table_args__ = (
        CheckConstraint(
            "number >= 1",
            name="number_positive",
        ),
        CheckConstraint(
            "planned_shots IS NULL OR planned_shots > 0",
            name="planned_shots_positive",
        ),
        CheckConstraint(
            "revision >= 0",
            name="revision_non_negative",
        ),
        CheckConstraint(
            "status IN ('created', 'active', 'completed', 'cancelled')",
            name="status_valid",
        ),
        Index(
            "uq_series_session_number",
            "session_id",
            "number",
            unique=True,
        ),
        Index("ix_series_session_id", "session_id"),
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("shooting_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    planned_shots: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="created",
        server_default=text("'created'"),
    )

    revision: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    session: Mapped["ShootingSession"] = relationship(
        back_populates="series",
    )

    shots: Mapped[list["Shot"]] = relationship(
        back_populates="series",
    )

    metrics_snapshots: Mapped[list["MetricsSnapshot"]] = relationship(
        back_populates="series",
    )