import pytest
from fastapi.testclient import TestClient
from app.main import app

# pytest-asyncio 설정
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="module")
def client():
    # 테스트용 클라이언트를 생성합니다.
    with TestClient(app) as c:
        yield c

