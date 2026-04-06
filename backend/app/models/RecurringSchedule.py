from datetime import datetime, date
from typing import Optional
 
from sqlalchemy import (
    Boolean, Date, Enum, ForeignKey, Index, Integer, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from enums import SchedulesFrequency

class Base(DeclarativeBase):
    pass

class RecurringSchedule(Base):
    __tablename__ = "recurring_schedules"
 
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.transaction_id"), nullable=False)
    frequency: Mapped[SchedulesFrequency] = mapped_column(Enum(SchedulesFrequency), nullable=False)
    next_run_at: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
 
    __table_args__ = (
        UniqueConstraint("transaction_id", name="uq_recurring_schedules_transaction_id"),
        CheckConstraint(
            "end_date IS NULL OR end_date >= next_run_at::date",
            name="ck_recurring_schedules_end_date_after_next_run",
        ),
        Index("ix_recurring_schedules_transaction_id", "transaction_id"),
    )
 
    transaction: Mapped["Transaction"] = relationship(back_populates="recurring_schedules")

    @validates("end_date")
    def validate_end_date(self, _key: str, value: Optional[date]) -> Optional[date]:
        if value is not None and self.next_run_at and value < self.next_run_at.date():
            raise ValueError("end_date must be on or after next_run_at")
        return value