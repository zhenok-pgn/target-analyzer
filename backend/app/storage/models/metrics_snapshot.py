from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, UUIDPrimaryKeyMixin


class MetricsSnapshot(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "metrics_snapshots"

    __table_args__ = (
        CheckConstraint(
            """
            (
                series_id IS NOT NULL
                AND session_id IS NULL
            )
            OR
            (
                series_id IS NULL
                AND session_id IS NOT NULL
            )
            """,
            name="ck_metrics_snapshots_single_owner",
        ),
        CheckConstraint(
            "revision >= 0",
            name="ck_metrics_snapshots_revision_non_negative",
        ),
    )

    series_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("series.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shooting_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    revision: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    metrics: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    series = relationship(
        "Series",
        back_populates="metrics_snapshots",
    )

    session = relationship(
        "ShootingSession",
        back_populates="metrics_snapshots",
    )