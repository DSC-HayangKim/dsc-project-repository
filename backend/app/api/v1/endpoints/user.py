from fastapi import APIRouter, Request, Depends, HTTPException
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.core.responses import APIResponse

router = APIRouter()

@router.get("/info")
async def get_user_info(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return APIResponse.create(status_code=401, message="No access token found")
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    user_id = decode_access_token(token)
    if not user_id:
        return APIResponse.create(status_code=401, message="Invalid access token")

    user_service = UserService()
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        return APIResponse.create(status_code=404, message="User not found")

    return APIResponse.create(status_code=200, data=user)
