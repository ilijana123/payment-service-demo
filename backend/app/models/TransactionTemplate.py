from datetime import datetime
from decimal import Decimal
from typing import Optional
 
from sqlalchemy import (
    Index, Integer,
    Numeric, String, Text, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TransactionTemplate(Base):
    __tablename__ = "transaction_templates"
 
    template_id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True, unique = True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable = False)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.card_id", ondelete="CASCADE"), nullable = False)
    name: Mapped[str] = mapped_column(Text, nullable = False, comment="user-defined label for the template")
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default = "USD", nullable = False)
    recipient: Mapped[str] = mapped_column(Text, nullable = False)
    reference: Mapped[Optional[str]] = mapped_column(Text, nullable = True)
    created_at: Mapped[datetime] = mapped_column(nullable = False)
    updated_at: Mapped[datetime] = mapped_column(nullable = False)
 
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_templates_amount_positive"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_templates_currency_format"),
        CheckConstraint("length(trim(recipient)) > 0", name="ck_templates_recipient_nonempty"),
        CheckConstraint("length(trim(name)) > 0", name="ck_templates_name_nonempty"),
        CheckConstraint("length(trim(name)) <= 100", name="ck_templates_name_maxlen"),
        CheckConstraint("updated_at >= created_at", name="ck_templates_updated_after_created"),
        Index("ix_transaction_templates_user_id", "user_id"),
        Index("ix_transaction_templates_card_id", "card_id")
    )
 
    user: Mapped["User"] = relationship(back_populates = "transaction_templates")
    card: Mapped["Card"] = relationship(back_populates = "transaction_templates")