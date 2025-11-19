from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from app.models.base import Base

class PatentEmbedding(Base):
    __tablename__ = "patent_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB) # metadata is reserved in SQLAlchemy
    embedding: Mapped[list[float]] = mapped_column(Vector(1536)) # Assuming OpenAI embedding dimension, can be changed
