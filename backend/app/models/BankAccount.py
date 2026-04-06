from decimal import Decimal
from sqlalchemy import (
    Enum, ForeignKey, Index, Integer,
    Numeric, String, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from enums import BankAccountStatus

class Base(DeclarativeBase):
    pass

class BankAccount(Base):
    __table__name = "bank_accounts"
 
    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete = "CASCADE"), unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[BankAccountStatus] = mapped_column(Enum(BankAccountStatus), nullable=False)
 
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_bank_account_user_id"), 
        CheckConstraint("balance >= 0", name="ck_bank_account_balance_positive"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_bank_account_currency_format"),
        Index("ix_bank_account_user_id", "user_id"),
    )

    user: Mapped["User"] = relationship(back_populates="bank_account")
    cards: Mapped[list["Card"]] = relationship(back_populates="account")

    @validates("balance")
    def validate_balance(self, _key: str, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        return value
 
    @validates("currency")
    def validate_currency(self, _key: str, value: str) -> str:
        value = value.upper().strip()
        if len(value) != 3 or not value.isalpha():
            raise ValueError(f"currency must be a 3-letter ISO 4217 code, got '{value}'")
        return value
