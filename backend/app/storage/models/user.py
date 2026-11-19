from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from app.storage.models.shooting_session import ShootingSession
    from app.storage.models.shot_revision import ShotRevision
    from app.storage.models.target_profile import TargetProfile


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    __table_args__ = (
        Index(
            "uq_users_login_lower",
            text("lower(login)"),
            unique=True,
        ),
    )

    login: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    shooting_sessions: Mapped[list["ShootingSession"]] = relationship(
        back_populates="user",
    )

    target_profiles: Mapped[list["TargetProfile"]] = relationship(
        back_populates="owner",
    )

    shot_revisions: Mapped[list["ShotRevision"]] = relationship(
        back_populates="user",
    )