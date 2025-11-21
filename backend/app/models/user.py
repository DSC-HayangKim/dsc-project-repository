import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.thread import Thread

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    profile_image: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)

    # Relationships
    threads: Mapped[List["Thread"]] = relationship(back_populates="user", cascade="all, delete-orphan")
