from fastapi import APIRouter, Request, Depends, HTTPException
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.core.responses import APIResponse
from app.api.deps import get_current_user_payload

router = APIRouter()

@router.get("/info")
async def get_user_info(user_id: str = Depends(get_current_user_payload)):
    """
    현재 로그인한 사용자의 정보를 조회합니다.
    쿠키에 있는 access_token을 사용하여 사용자를 식별합니다.
    
    Args:
        user_id (str): 현재 사용자 ID (Dependency injection).
        
    Returns:
        APIResponse: 사용자 정보가 담긴 응답 객체.
    """
    user_service = UserService()
    user = await user_service.get_user_by_id(int(user_id))
    
    if not user:
        return APIResponse.create(status_code=404, message="User not found")

    return APIResponse.create(status_code=200, data=user)
