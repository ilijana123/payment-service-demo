from datetime import datetime
from sqlalchemy import (
    Boolean, Enum, ForeignKey, Index, Integer,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enums import CardReportType

class Base(DeclarativeBase):
    pass

class CardReport(Base):
    __tablename__ = "card_reports"
 
    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.card_id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    report_type: Mapped[CardReportType] = mapped_column(Enum(CardReportType), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="email OTP confirmed")
    created_at: Mapped[datetime] = mapped_column(nullable=False)
 
    __table_args__ = (
        Index("ix_card_reports_user_id", "user_id"),
        Index("ix_card_reports_card_id", "card_id"),
    )
 
    card: Mapped["Card"] = relationship(back_populates="card_reports")
    user: Mapped["User"] = relationship(back_populates="card_reports")