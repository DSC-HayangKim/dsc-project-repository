from sqlalchemy import String, Integer, Text, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from app.models.base import Base 


class Patent(Base):
    __tablename__ = "patents"

    # 1. PRIMARY KEY: _id (VARCHAR(24))
    # MongoDB ObjectId의 문자열 표현을 그대로 사용합니다.
    _id: Mapped[str] = mapped_column(String(24), primary_key=True)

    # 2. VARCHAR 컬럼들
    applicant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    application_number: Mapped[str] = mapped_column(String(255), unique=True)
    invention_title: Mapped[str] = mapped_column(String(511))
    ipc_number: Mapped[str] = mapped_column(String(255))
    open_number: Mapped[str] = mapped_column(String(255))
    publication_number: Mapped[str] = mapped_column(String(255))
    register_number: Mapped[str] = mapped_column(String(255), unique=True)
    register_status: Mapped[str] = mapped_column(String(50))

    # 3. DATE 컬럼들
    application_date: Mapped[Date] = mapped_column(Date, nullable=True) # None 허용
    open_date: Mapped[Date] = mapped_column(Date, nullable=True)
    publication_date: Mapped[Date] = mapped_column(Date, nullable=True)
    register_date: Mapped[Date] = mapped_column(Date, nullable=True)

    # 4. TEXT 컬럼들
    abstract_content: Mapped[str] = mapped_column(Text)
    description_v1: Mapped[str] = mapped_column(Text)
    big_drawing_url: Mapped[str] = mapped_column(Text)
    drawing_url: Mapped[str] = mapped_column(Text)

    # 5. INTEGER 컬럼
    index_no: Mapped[int] = mapped_column(Integer)

    # 6. VECTOR 컬럼
    # `vector(768)` 타입에 맞춰 `Vector(768)`로 정의
    embedding: Mapped[list[float]] = mapped_column(Vector(768))

    # 기타: ORM 객체를 출력할 때 유용한 __repr__ 메서드 (선택 사항)
    def __repr__(self):
        return (
            f"Patent("
            f"_id='{self._id}', "
            f"application_number='{self.application_number}', "
            f"invention_title='{self.invention_title[:50]}...')"
        )