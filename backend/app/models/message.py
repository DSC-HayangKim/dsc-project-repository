
from datetime import datetime
from sqlalchemy import String, ForeignKey, func, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.thread import Thread

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String)  # e.g., 'user', 'assistant'
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    thread: Mapped["Thread"] = relationship(back_populates="messages")
