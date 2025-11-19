from fastapi import APIRouter
from typing import List
from app.crud import thread as crud_thread
from app.schemas import thread as schema_thread

router = APIRouter()

# 최근 스레드 조회 API
@router.get("/", response_model=List[schema_thread.Thread])
async def read_threads(
    skip: int = 0,
    limit: int = 100
):
    """
    최근 스레드 목록을 조회합니다.
    """
    return await crud_thread.get_threads(skip=skip, limit=limit)
