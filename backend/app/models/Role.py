from sqlalchemy import (
    Integer, String, CheckConstraint
)
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass
 
class Role(Base):
    __tablename__ = "roles"
 
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False, comment="visitor, user, admin")

    users: Mapped[list["User"]] = relationship(back_populates="role")
    