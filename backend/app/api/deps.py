from fastapi import Request, HTTPException, status
from app.core.security import decode_access_token
from app.core import settings

async def get_current_user_payload(request: Request) -> str:
    """
    쿠키에서 액세스 토큰을 추출하고 유효성을 검사한 후 사용자 ID(payload)를 반환합니다.
    
    Args:
        request (Request): 들어오는 요청 객체.
        
    Returns:
        str: 토큰에서 추출된 사용자 ID.
        
    Raises:
        HTTPException: 토큰이 없거나 유효하지 않은 경우 발생합니다.
    """
    if (settings.DEV_MODE == "development"):
        return "2"

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token found",
        )
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    payload = decode_access_token(token)
    if not payload or not payload.sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
        
    return str(payload.sub)
