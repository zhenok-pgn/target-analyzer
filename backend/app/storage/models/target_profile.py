from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from app.storage.models.target_profile_version import TargetProfileVersion
    from app.storage.models.shooting_session import ShootingSession
    from app.storage.models.user import User


class TargetProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "target_profiles"

    __table_args__ = (
        Index(
            "uq_target_profiles_owner_name",
            "owner_id",
            "name",
            unique=True,
            postgresql_where=text("owner_id IS NOT NULL"),
        ),
        Index(
            "uq_target_profiles_builtin_name",
            "name",
            unique=True,
            postgresql_where=text("owner_id IS NULL"),
        ),
    )

    owner_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    target_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    is_builtin: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )

    owner: Mapped["User | None"] = relationship(
        back_populates="target_profiles",
    )

    versions: Mapped[list["TargetProfileVersion"]] = relationship(
        back_populates="profile",
    )