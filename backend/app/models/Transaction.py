from datetime import datetime
from decimal import Decimal
from typing import Optional
 
from sqlalchemy import (
    Enum, ForeignKey, Index, Integer,
    Numeric, String, Text, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from enums import TransactionStatus, TransactionType

class Base(DeclarativeBase):
    pass

class Transaction(Base):
    __tablename__ = "transactions"
 
    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.card_id", ondelete="RESTRICT"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    recipient: Mapped[str] = mapped_column(Text, nullable=False)
    reference: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
 
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_transactions_currency_format"),
        CheckConstraint("length(trim(recipient)) > 0", name="ck_transactions_recipient_nonempty"),
        Index("ix_transactions_user_id", "user_id"),
        Index("ix_transactions_card_id", "card_id"),
    )
 
    user: Mapped["User"] = relationship(back_populates="transactions")
    card: Mapped["Card"] = relationship(back_populates="transactions")
    recurring_schedules: Mapped[list["RecurringSchedule"]] = relationship(back_populates="transaction")
    transaction_logs: Mapped[list["TransactionLog"]] = relationship(back_populates="transaction")

    @validates("amount")
    def validate_amount(self, _key: str, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError(f"Transaction amount must be > 0, got {value}")
        return value
 
    @validates("currency")
    def validate_currency(self, _key: str, value: str) -> str:
        value = value.upper().strip()
        if len(value) != 3 or not value.isalpha():
            raise ValueError(f"currency must be a 3-letter ISO 4217 code, got '{value}'")
        return value
 
    @validates("recipient")
    def validate_recipient(self, _key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("recipient must not be blank")
        return value