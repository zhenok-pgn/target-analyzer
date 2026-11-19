from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.storage.models.shooting_session import ShootingSession
    from app.storage.models.shot import Shot


class MediaAsset(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "media_assets"

    __table_args__ = (
        UniqueConstraint(
            "storage_path",
            name="uq_media_assets_storage_path",
        ),
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("shooting_sessions.id"),
        nullable=False,
        index=True,
    )

    asset_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    original_filename: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    sha256: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    retention_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    session: Mapped["ShootingSession"] = relationship(
        back_populates="media_assets",
    )

    shots: Mapped[list["Shot"]] = relationship(
        back_populates="media_asset",
    )