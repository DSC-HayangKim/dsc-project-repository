# 백엔드 API 문서

## 인증 (Authentication)

대부분의 API 엔드포인트는 인증이 필요합니다. 인증은 `access_token`이라는 이름의 HTTP-only 쿠키에 저장된 JWT 토큰을 통해 이루어집니다.

## API 엔드포인트

### 인증 (Auth) - `/api/v1/auth`

#### `GET /google/login`

- **설명**: Google OAuth2 로그인 절차를 시작합니다.
- **응답**: Google 로그인 페이지로 리다이렉트됩니다.

#### `GET /google/callback`

- **설명**: Google OAuth2 콜백 URL입니다. Google에서 받은 인증 코드를 검증하고, 사용자를 생성하거나 조회한 뒤 `access_token` 쿠키를 설정합니다.
- **응답**: 프론트엔드 루트 페이지(`/`)로 리다이렉트됩니다.

### 사용자 (User) - `/api/v1/user`

#### `GET /info`

- **설명**: 현재 로그인한 사용자의 정보를 조회합니다.
- **인증**: 필수 (`access_token` 쿠키 필요).
- **응답**: 사용자 세부 정보가 담긴 JSON 객체를 반환합니다.

### 스레드 (Threads) - `/api/v1/threads`

_`get_current_user_payload` 의존성을 통해 보호됩니다._

#### `GET /`

- **설명**: 최근 스레드 목록을 조회합니다.
- **인증**: 필수 (`access_token` 쿠키 필요).
- **쿼리 파라미터**:
  - `skip` (int, 기본값: 0): 건너뛸 레코드 수.
  - `limit` (int, 기본값: 100): 반환할 최대 레코드 수.
- **응답**: 스레드 객체들의 리스트를 반환합니다.

#### `POST /create`

- **설명**: 현재 사용자를 위한 새로운 스레드를 생성합니다.
- **인증**: 필수 (`access_token` 쿠키 필요).
- **응답**: 생성된 스레드 객체를 반환합니다.

### 채팅 (Chat) - `/api/v1/chat`

_`get_current_user_payload` 의존성을 통해 보호됩니다._

#### `POST /`

- **설명**: 에이전트에게 메시지를 보내고 스트리밍 응답을 받습니다. 사용자 메시지와 에이전트 응답은 데이터베이스에 저장됩니다.
- **인증**: 필수 (`access_token` 쿠키 필요).
- **요청 본문 (Body)** (`application/json`):
  ```json
  {
    "message": "사용자가 보낼 메시지 내용",
    "session_id": 123 // 스레드 ID (Integer)
  }
  ```
- **응답**: 텍스트 스트리밍 (`text/plain`). 에이전트의 응답이 실시간으로 전송됩니다.

### 에이전트 (Agent) - `/api/v1/agent`

_`get_current_user_payload` 의존성을 통해 보호됩니다._

#### `POST /chat`

- **설명**: 에이전트와 일반적인(비스트리밍) 대화를 나눕니다.
- **인증**: 필수 (`access_token` 쿠키 필요).
- **요청 본문 (Body)** (`application/json`):
  ```json
  {
    "query": "질문 내용",
    "llm_type": "openai" // 또는 "ollama"
  }
  ```
- **응답**: 에이전트의 응답 텍스트가 담긴 JSON 객체를 반환합니다.
