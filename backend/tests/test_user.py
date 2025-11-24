import pytest
from unittest.mock import AsyncMock, patch
from app.core.responses import APIResponse
from app.core.security import create_access_token
from datetime import timedelta

# Mock 페이로드 클래스 정의
class MockPayload:
    def __init__(self, sub):
        self.sub = sub

@patch("app.api.v1.endpoints.user.decode_access_token")
def test_get_user_info_success(mock_decode_token, client):
    # Mock 설정
    mock_decode_token.return_value = MockPayload(sub="2")

    # 요청 보내기
    response = client.get("/api/v1/user/info", cookies={"access_token": create_access_token(subject="2", expires_delta=timedelta(minutes=1))})

    # 검증
    assert response.status_code == 200
    data = response.json()
    assert data["status_code"] == 200
    assert data["data"]["email"] == "hhs200306@gmail.com"

def test_get_user_info_no_token(client):
    response = client.get("/api/v1/user/info")
    assert response.status_code == 401
    assert response.json()["message"] == "No access token found"
    assert response.json()['status_code'] == 401

@patch("app.api.v1.endpoints.user.decode_access_token")
def test_get_user_info_invalid_token(mock_decode_token, client):
    mock_decode_token.return_value = None
    
    response = client.get("/api/v1/user/info", cookies={"access_token": create_access_token(subject="-1", expires_delta=timedelta(minutes=1))})

    # 없는 유저 이기 때문에, forbidden이 발생한다.
    
    assert response.status_code == 401
    assert response.json()["data"] == None
