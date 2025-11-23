from typing import List, Any
from app.db.client import supabase
from app.schemas.thread import Thread

# 최근 스레드 조회 함수
async def get_threads(skip: int = 0, limit: int = 100) -> List[Thread]:
    """
    모든 스레드를 생성일 기준 내림차순으로 조회합니다.
    Supabase Client를 직접 사용하여 데이터를 조회합니다.
    
    Args:
        skip (int): 건너뛸 항목 수 (기본값: 0).
        limit (int): 반환할 항목 수 (기본값: 100).
        
    Returns:
        List[Thread]: 조회된 스레드 객체 리스트.
    """
    # Supabase table select
    response = supabase.table("threads") \
        .select("*") \
        .order("created_at", desc=True) \
        .range(skip, skip + limit - 1) \
        .execute()

    # Pydantic 모델로 변환
    return [Thread(**item) for item in response.data]

# 스레드 생성 함수
async def create_thread(user_id: int) -> Thread:
    """
    새로운 스레드를 생성합니다.
    
    Args:
        user_id (int): 스레드를 생성할 사용자의 ID.
        
    Returns:
        Thread: 생성된 스레드 객체. 생성 실패 시 None 반환.
    """
    response = supabase.table("threads").insert({"user_id": user_id}).execute()
    
    if not response.data:
        return None
        
    return Thread(**response.data[0])
