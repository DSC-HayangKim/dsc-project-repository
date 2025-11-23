from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
from app.core import settings

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    JWT 액세스 토큰을 생성합니다.
    
    Args:
        subject (Union[str, Any]): 토큰의 주체 (보통 사용자 ID).
        expires_delta (timedelta, optional): 토큰 만료 시간. 지정하지 않으면 기본값이 사용됩니다.
        
    Returns:
        str: 생성된 JWT 문자열.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Union[str, Any]:
    """
    JWT 액세스 토큰을 디코딩하고 검증합니다.
    
    Args:
        token (str): 디코딩할 JWT 문자열.
        
    Returns:
        Union[str, Any]: 토큰의 주체 (sub claim). 유효하지 않은 경우 None 반환.
    """
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_jwt.get("sub")
    except jwt.PyJWTError:
        return None
