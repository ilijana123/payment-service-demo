from datetime import datetime
from typing import Optional
 
from sqlalchemy import (
    ForeignKey, Index, Integer, String, Text, Enum
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from enums import TransactionStatus

class Base(DeclarativeBase):
    pass 

class TransactionLog(Base):
    __tablename__ = "transaction_logs"
 
    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.transaction_id", ondelete="CASCADE"), nullable=False)
    old_status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), nullable=False)
    new_status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), nullable=False)
    error_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    error_code_description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    error_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
 
    __table_args__ = (
        Index("ix_transaction_logs_user_id", "user_id"),
        Index("ix_transaction_logs_transaction_id", "transaction_id"),
    )
 
    user: Mapped["User"] = relationship(back_populates="transaction_logs")
    transaction: Mapped["Transaction"] = relationship(back_populates="transaction_logs")

    @validates("old_status", "new_status")
    def validate_status_values(self, key: str, value: str) -> str:
        allowed = {s.value for s in TransactionStatus}
        if value not in allowed:
            raise ValueError(f"{key} '{value}' is not a valid TransactionStatus")
        return value