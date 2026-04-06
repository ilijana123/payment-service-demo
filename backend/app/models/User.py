from datetime import datetime
from typing import Optional
 
from sqlalchemy import (
    Boolean, ForeignKey, Index, Integer, Text, UniqueConstraint, CheckConstraint
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
 
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("role.role_id", ondelete="RESTRICT"), nullable=False
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
 
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        CheckConstraint("length(trim(name))  > 0", name="ck_users_name_nonempty"),
        CheckConstraint("length(trim(email)) > 0", name="ck_users_email_nonempty"),
        CheckConstraint("email LIKE '%@%.%'",      name="ck_users_email_format"),
        Index("ix_users_role_id", "role_id"),
        Index("ix_users_email",   "email"),
    )
 
    role: Mapped["Role"] = relationship(back_populates="users")
    bank_account: Mapped[Optional["BankAccount"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
    transaction_templates: Mapped[list["TransactionTemplate"]] = relationship(back_populates="user")
    card_reports: Mapped[list["CardReport"]] = relationship(back_populates="user")
    email_verifications: Mapped[list["EmailVerification"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    transaction_logs: Mapped[list["TransactionLog"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
 
    @validates("email")
    def validate_email(self, _key: str, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError(f"Invalid email address: '{value}'")
        return value
 
    @validates("name")
    def validate_name(self, _key: str, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("User name must not be blank")
        if len(value) > 255:
            raise ValueError("User name exceeds 255 characters")
        return value
 
    @validates("password_hash")
    def validate_password_hash(self, _key: str, value: bytes) -> bytes:
        if not value or len(value) != 60:
            raise ValueError("password_hash must be a 60-byte bcrypt digest")
        return value
 

