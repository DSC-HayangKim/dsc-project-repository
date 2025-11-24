# 백엔드 테스트

이 디렉토리는 백엔드 애플리케이션을 위한 테스트 코드를 포함하고 있습니다.

## 사전 준비

테스트 의존성이 설치되어 있는지 확인하세요:

```bash
pip install -r ../requirements.txt
```

## 테스트 실행

모든 테스트를 실행하려면 `backend` 디렉토리에서 다음 명령어를 실행하세요:

```bash
pytest
```

특정 테스트 파일을 실행하려면:

```bash
pytest tests/test_user.py
```

## 구조

- `conftest.py`: pytest 픽스처(예: `client`)를 포함합니다.
- `test_*.py`: 테스트 파일들입니다.
