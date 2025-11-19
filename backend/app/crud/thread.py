from typing import List, Any
from app.db.client import supabase
from app.schemas.thread import Thread

# 최근 스레드 조회 함수
async def get_threads(skip: int = 0, limit: int = 100) -> List[Thread]:
    """
    모든 스레드를 생성일 기준 내림차순으로 조회합니다.
    Supabase Client를 직접 사용하여 데이터를 조회합니다.
    """
    # Supabase table select
    response = supabase.table("threads") \
        .select("*") \
        .order("created_at", desc=True) \
        .range(skip, skip + limit - 1) \
        .execute()

    # Pydantic 모델로 변환
    return [Thread(**item) for item in response.data]
