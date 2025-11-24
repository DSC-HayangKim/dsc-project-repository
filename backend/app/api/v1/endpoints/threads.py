from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.services.thread_service import ThreadService
from app.schemas import thread as schema_thread
from app.api.deps import get_current_user_payload

router = APIRouter()

# 최근 스레드 조회 API
@router.get("/", response_model=List[schema_thread.Thread])
async def read_threads(
    skip: int = 0,
    limit: int = 20,
    user_id: str = Depends(get_current_user_payload)
):
    """
    최근 스레드 목록을 조회합니다.
    
    Args:
        skip (int): 건너뛸 항목 수 (기본값: 0).
        limit (int): 반환할 항목 수 (기본값: 100).
        user_id (str): 현재 사용자 ID (Dependency injection).
        
    Returns:
        List[schema_thread.Thread]: 조회된 스레드 목록.
    """
    return await ThreadService.get_threads(user_id=int(user_id), skip=skip, limit=limit)

@router.post("/create", response_model=schema_thread.Thread)
async def create_new_thread(
    user_id: str = Depends(get_current_user_payload)
):
    """
    새로운 스레드를 생성합니다.
    access_token 쿠키를 통해 사용자를 식별하고 해당 사용자의 스레드를 생성합니다.
    
    Args:
        user_id (str): 현재 사용자 ID (Dependency injection).
        
    Returns:
        schema_thread.Thread: 생성된 스레드 객체.
        
    Raises:
        HTTPException: 인증 실패 또는 생성 실패 시 발생.
    """
    thread = await ThreadService.create_thread(user_id=int(user_id))
    if not thread:
        raise HTTPException(status_code=500, detail="Failed to create thread")
        
    return thread
