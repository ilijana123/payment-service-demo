from datetime import datetime
from sqlalchemy import (
    Boolean, Enum, ForeignKey, Index, Integer, Text, CheckConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enums import EmailVerificationPurpose

class Base(DeclarativeBase):
    pass

class EmailVerification(Base):
    __tablename__ = "email_verifications"
 
    verification_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False, comment="OTP or UUID link")
    purpose: Mapped[EmailVerificationPurpose] = mapped_column(Enum(EmailVerificationPurpose), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
 
    __table_args__ = (
        CheckConstraint("length(trim(token)) > 0", name="ck_email_verification_token_nonempty"),
        Index("ix_email_verification_user_id", "user_id")
    )
    
    user: Mapped["User"] = relationship(back_populates="email_verifications")