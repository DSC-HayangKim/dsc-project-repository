
from datetime import datetime
from sqlalchemy import String, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.models.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message

class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    title: Mapped[str | None] = mapped_column(String, nullable=True)

    # timestampz를 사용하는 것이 맞습니다.
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="threads")
    messages: Mapped[List["Message"]] = relationship(back_populates="thread", cascade="all, delete-orphan")
