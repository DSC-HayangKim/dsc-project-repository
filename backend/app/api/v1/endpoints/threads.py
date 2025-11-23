from fastapi import APIRouter
from typing import List
from app.crud import thread as crud_thread
from app.schemas import thread as schema_thread
from fastapi import APIRouter, Request, HTTPException
from app.core.security import decode_access_token

router = APIRouter()

# 최근 스레드 조회 API
@router.get("/", response_model=List[schema_thread.Thread])
async def read_threads(
    skip: int = 0,
    limit: int = 100
):
    """
    최근 스레드 목록을 조회합니다.
    
    Args:
        skip (int): 건너뛸 항목 수 (기본값: 0).
        limit (int): 반환할 항목 수 (기본값: 100).
        
    Returns:
        List[schema_thread.Thread]: 조회된 스레드 목록.
    """
    return await crud_thread.get_threads(skip=skip, limit=limit)

@router.post("/create", response_model=schema_thread.Thread)
async def create_new_thread(request: Request):
    """
    새로운 스레드를 생성합니다.
    access_token 쿠키를 통해 사용자를 식별하고 해당 사용자의 스레드를 생성합니다.
    
    Args:
        request (Request): 요청 객체 (쿠키 포함).
        
    Returns:
        schema_thread.Thread: 생성된 스레드 객체.
        
    Raises:
        HTTPException: 인증 실패 또는 생성 실패 시 발생.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No access token found")
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid access token")

    thread = await crud_thread.create_thread(user_id=int(user_id))
    if not thread:
        raise HTTPException(status_code=500, detail="Failed to create thread")
        
    return thread
