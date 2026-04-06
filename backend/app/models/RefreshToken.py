import uuid
import enum
from datetime import datetime
from typing import Optional
 
from sqlalchemy import (
    ForeignKey, Index, Integer, Text, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
 
    token_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4, unique = True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    refresh_token_hash: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    jti: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    replaced_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
 
    __table_args__ = (
        CheckConstraint("expires_at > created_at", name="ck_refresh_token_expiry_after_created"),
        CheckConstraint(
            "revoked_at IS NULL OR revoked_at >= created_at",
            name="ck_refresh_token_revoked_after_created",
        ),
        CheckConstraint("length(trim(jti)) > 0", name="ck_refresh_token_jti_nonempty"),
        CheckConstraint("length(trim(refresh_token_hash)) > 0",name="ck_refresh_token_hash_nonempty"),
        Index("ix_refresh_token_user_id",    "user_id"),
    )
 
    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
 