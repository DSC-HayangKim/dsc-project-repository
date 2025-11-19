# Backend Directory Structure Guide (Korean)

이 문서는 FastAPI 백엔드 프로젝트의 디렉토리 구조와 각 폴더의 역할을 설명합니다.

## 📂 디렉토리 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # 애플리케이션 진입점 (Entry Point)
│   ├── api/             # API 엔드포인트 (Router)
│   │   ├── __init__.py
│   │   └── v1/          # API 버전 관리
│   │       ├── __init__.py
│   │       └── endpoints/ # 실제 API 로직 구현
│   ├── core/            # 핵심 설정 및 공통 기능
│   │   ├── __init__.py
│   │   └── config.py    # 환경 변수 및 설정 관리
│   ├── db/              # 데이터베이스 관련 코드
│   │   ├── __init__.py
│   │   └── session.py   # DB 세션 관리
│   ├── models/          # 데이터베이스 모델 (ORM)
│   │   └── __init__.py
│   ├── schemas/         # Pydantic 스키마 (DTO)
│   │   └── __init__.py
│   └── crud/            # CRUD 작업 (DB 접근 로직)
│       └── __init__.py
├── tests/               # 테스트 코드
├── dockerfile.prod      # 배포용 Dockerfile
└── requirements.txt     # 의존성 패키지 목록
```

## 📝 각 폴더별 역할 및 가이드라인

### `app/main.py`
- **역할**: FastAPI 애플리케이션 객체(`app`)를 생성하고 실행하는 파일입니다.
- **내용**: 미들웨어 설정, 라우터 등록, 예외 처리 핸들러 등록 등을 수행합니다.

### `app/api/`
- **역할**: 클라이언트의 요청을 받아 처리하고 응답을 반환하는 API 엔드포인트를 정의합니다.
- **가이드라인**:
    - `v1/` 폴더를 사용하여 API 버전을 관리합니다.
    - `endpoints/` 폴더 내에 기능별로 파일(예: `users.py`, `items.py`)을 나누어 라우터를 정의합니다.
    - 비즈니스 로직은 가능한 `crud/` 또는 서비스 계층으로 분리하여 컨트롤러(라우터)를 가볍게 유지합니다.

### `app/core/`
- **역할**: 프로젝트 전반에서 사용되는 핵심 설정과 유틸리티를 포함합니다.
- **내용**:
    - `config.py`: `pydantic-settings`를 사용하여 환경 변수를 로드하고 관리합니다.
    - `security.py`: JWT 토큰 생성, 비밀번호 해싱 등 보안 관련 함수.

### `app/db/`
- **역할**: 데이터베이스 연결 및 세션 관리를 담당합니다.
- **내용**: `session.py` 또는 `base.py`에서 SQLAlchemy 엔진과 세션 메이커를 생성합니다.

### `app/models/`
- **역할**: 데이터베이스 테이블과 매핑되는 ORM 모델(SQLAlchemy 모델)을 정의합니다.
- **가이드라인**: 각 테이블별로 클래스를 정의하고, `Base` 클래스를 상속받습니다.

### `app/schemas/`
- **역할**: 데이터 유효성 검사 및 직렬화/역직렬화를 위한 Pydantic 모델(DTO)을 정의합니다.
- **가이드라인**: 요청(Request) 스키마와 응답(Response) 스키마를 명확히 구분하여 작성합니다 (예: `UserCreate`, `UserResponse`).

### `app/crud/`
- **역할**: 데이터베이스에 직접 접근하여 데이터를 생성, 조회, 수정, 삭제(CRUD)하는 로직을 담당합니다.
- **가이드라인**: API 라우터에서 직접 DB 쿼리를 작성하지 않고, CRUD 함수를 호출하여 사용합니다.

## 🚀 개발 가이드

1. **새로운 기능 추가 시**:
    - `models/`에 DB 모델 정의 (필요한 경우)
    - `schemas/`에 입출력 스키마 정의
    - `crud/`에 DB 조작 로직 구현
    - `api/v1/endpoints/`에 API 라우터 구현
    - `main.py` 또는 `api/v1/api.py`에 라우터 등록

2. **코딩 스타일**:
    - Type Hinting을 적극적으로 사용합니다.
    - 비동기 처리(`async def`)를 기본으로 사용합니다.
