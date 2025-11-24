import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.schemas.message import ChatRequest
from app.api.deps import get_current_user_payload

client = TestClient(app)

@pytest.fixture
def mock_current_user():
    """Mock the authentication dependency using FastAPI's dependency_overrides."""
    async def override_get_current_user():
        return "test_user"
    
    app.dependency_overrides[get_current_user_payload] = override_get_current_user
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def mock_message_service():
    """Mock the MessageService.process_chat to return a simple async generator."""
    async def mock_generator(*args, **kwargs):
        yield "Mocked vector DB result"
    
    with patch('app.services.message_service.MessageService.process_chat', 
               return_value=mock_generator()):
        yield

def test_chat_endpoint_returns_vector_db_result(mock_current_user, mock_message_service):
    request_payload = {
        "session_id": 1,
        "message": "항공기문을 좀더 견고하면서도 가벼운 소재로 바꾸고 싶어 관련된 특허 없어?"
    }
    response = client.post("/api/v1/chat/", json=request_payload)
    assert response.status_code == 200
    # The response is a streaming text/plain; read the content
    content = response.content.decode()
    assert "Mocked vector DB result" in content
