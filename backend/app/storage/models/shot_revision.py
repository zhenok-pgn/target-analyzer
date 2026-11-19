from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.storage.models.shot import Shot
    from app.storage.models.user import User


class ShotRevision(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "shot_revisions"

    __table_args__ = (
        UniqueConstraint(
            "shot_id",
            "revision_number",
            name="uq_shot_revisions_shot_revision_number",
        ),
    )

    shot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("shots.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    revision_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    changed_fields: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    previous_values: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    new_values: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    shot: Mapped["Shot"] = relationship(
        back_populates="revisions",
    )

    user: Mapped["User"] = relationship(
        back_populates="shot_revisions",
    )