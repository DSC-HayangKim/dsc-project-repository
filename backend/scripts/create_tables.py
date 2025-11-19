import asyncio
import sys
import os

# Add the backend directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.models.base import Base
# Import all models to ensure they are registered with Base.metadata
from app.models import User, Thread, Message

# 테이블을 만드는 함수
async def create_tables():
    async with engine.begin() as conn:
        # 금지된 라인함수 절대로 실행시키지 말것
        # await conn.run_sync(Base.metadata.drop_all) # Optional: Drop existing tables for clean slate during dev

        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
