from datetime import datetime
from sqlalchemy import (
    Boolean, Enum, ForeignKey, Index, Integer, Text, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enums import CardStatus

class Base(DeclarativeBase):
    pass

class Card(Base):
    __tablename__ = "cards"
 
    card_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    card_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("card_type.card_type_id", ondelete = "RESTRICT"), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("bank_account.account_id", ondelete = "CASCADE"), nullable=False)
    card_number_masked: Mapped[str] = mapped_column(Text, nullable=False, comment="Last 4 digits only, e.g **** 4242")
    cardholder_name: Mapped[str] = mapped_column(Text, nullable=False)
    expiry_month: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[CardStatus] = mapped_column(Enum(CardStatus), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
 
    __table_args__ = (
        CheckConstraint("expiry_month BETWEEN 1 AND 12", name="ck_cards_expiry_month"),
        CheckConstraint("expiry_year >= 2026", name="ck_cards_expiry_year"),
        CheckConstraint(
            "card_number_masked ~ '^(\\*{4} )?[0-9]{4}$'",
            name="ck_cards_number_masked_format",
        ),
        CheckConstraint("length(trim(cardholder_name)) > 0", name="ck_cards_cardholder_nonempty"),
        Index("ix_cards_account_id",   "account_id"),
        Index("ix_cards_card_type_id", "card_type_id"),
    )
 
    card_type: Mapped["CardType"] = relationship(back_populates="cards")
    account: Mapped["BankAccount"] = relationship(back_populates="cards")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="card")
    transaction_templates: Mapped[list["TransactionTemplate"]] = relationship(back_populates="card")
    card_reports: Mapped[list["CardReport"]] = relationship(back_populates="card")
