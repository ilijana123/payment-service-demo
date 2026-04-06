from sqlalchemy import (
    Integer, String
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class CardType(Base):
    __tablename__ = "card_types"
 
    card_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    type: Mapped[str] = mapped_column(String, nullable=False, comment="visa, mastercard")
    
    cards: Mapped[list["Card"]] = relationship(back_populates="card_type")
