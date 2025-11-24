# 백엔드 API 문서

## 개요

본 문서는 Patent AI 백엔드의 모든 API 엔드포인트에 대한 상세한 설명을 제공합니다. 
Frontend 개발자는 이 문서만으로 모든 API 통합 작업을 수행할 수 있습니다.

**Base URL**: `/api/v1`

## 인증 (Authentication)

대부분의 API는 인증이 필요하며, `access_token`이라는 HTTP-only 쿠키에 저장된 JWT 토큰을 사용합니다.

- **쿠키 이름**: `access_token`
- **형식**: `Bearer {JWT_TOKEN}`
- **만료 시간**: 1800초 (30분)
- **HttpOnly**: true

---

## API 엔드포인트

### 1. 인증 (Auth) - `/api/v1/auth`

#### 1.1 Google 로그인 시작

```
GET /api/v1/auth/google/login
```

**설명**: Google OAuth2 로그인을 시작합니다.

**인증**: 불필요

**Request**: 없음

**Response**: Google 로그인 페이지로 리다이렉트

**사용 예시**:
```typescript
// Frontend에서 이 URL로 이동
window.location.href = "/api/v1/auth/google/login"
```

---

#### 1.2 Google OAuth 콜백

```
GET /api/v1/auth/google/callback
```

**설명**: Google OAuth2 콜백 처리. Google 인증 후 자동으로 호출되며, 사용자를 생성/조회하고 JWT 토큰을 쿠키에 설정합니다.

**인증**: 불필요 (Google이 제공하는 코드로 인증)

**Request**: Google에서 자동으로 제공하는 쿼리 파라미터

**Response**: 
- 성공 시: `/` (루트 페이지)로 리다이렉트하며, `access_token` 쿠키 설정
- 실패 시: `400` 에러

---

### 2. 사용자 (User) - `/api/v1/user`

#### 2.1 사용자 정보 조회

```
GET /api/v1/user/info
```

**설명**: 현재 로그인한 사용자의 정보를 조회합니다.

**인증**: 필수 (access_token 쿠키)

**Request**: 없음

**Response Body**:
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "display_name": "홍길동",
    "profile_image": "https://example.com/profile.jpg",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**에러 응답**:
```json
{
  "status_code": 401,
  "message": "No access token found",
  "data": null
}
```

---

### 3. 스레드 (Threads) - `/api/v1/threads`

#### 3.1 스레드 목록 조회

```
GET /api/v1/threads?skip=0&limit=20
```

**설명**: 현재 사용자의 스레드(대화 세션) 목록을 조회합니다.

**인증**: 필수 (access_token 쿠키)

**Query Parameters**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| skip | integer | 선택 | 0 | 건너뛸 항목 수 (페이지네이션) |
| limit | integer | 선택 | 20 | 반환할 최대 항목 수 |

**Response Body**:
```json
[
  {
    "id": 1,
    "title": "항공기 소재 특허 검색",
    "user_id": 123,
    "created_at": "2024-01-01T10:00:00"
  },
  {
    "id": 2,
    "title": null,
    "user_id": 123,
    "created_at": "2024-01-02T15:30:00"
  }
]
```

**Response 필드 설명**:
- `id`: 스레드 고유 ID
- `title`: 스레드 제목 (null일 수 있음, 기본값 "새로운 대화")
- `user_id`: 스레드 소유자 ID
- `created_at`: 생성 일시 (ISO 8601 형식)

---

#### 3.2 새 스레드 생성

```
POST /api/v1/threads/create
```

**설명**: 새로운 대화 스레드를 생성합니다.

**인증**: 필수 (access_token 쿠키)

**Request Body**: 없음

**Response Body**:
```json
{
  "id": 3,
  "title": null,
  "user_id": 123,
  "created_at": "2024-01-03T09:15:00"
}
```

**에러 응답**:
```json
{
  "detail": "Failed to create thread"
}
```
Status Code: `500`

---

#### 3.3 스레드의 메시지 목록 조회

```
GET /api/v1/threads/{thread_id}/messages
```

**설명**: 특정 스레드의 모든 메시지를 조회합니다.

**인증**: 필수 (access_token 쿠키)

**Path Parameters**:
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| thread_id | integer | 필수 | 조회할 스레드의 ID |

**Response Body**:
```json
[
  {
    "id": 1,
    "content": "항공기 소재 특허를 찾아줘",
    "role": "user",
    "created_at": "2024-01-01T10:00:00"
  },
  {
    "id": 2,
    "content": "항공기 소재와 관련된 특허를 검색해드리겠습니다...",
    "role": "assistant",
    "created_at": "2024-01-01T10:00:05"
  }
]
```

**Response 필드 설명**:
- `id`: 메시지 고유 ID
- `content`: 메시지 내용
- `role`: 메시지 작성자 (`user` 또는 `assistant`)
- `created_at`: 작성 일시 (ISO 8601 형식)

**에러 응답**:
```json
{
  "detail": "Thread not found"
}
```
Status Code: `404`

```json
{
  "detail": "Unauthorized"
}
```
Status Code: `403` (다른 사용자의 스레드에 접근 시)

---

### 4. 채팅 (Chat) - `/api/v1/chat`

#### 4.1 메시지 전송 (스트리밍)

```
POST /api/v1/chat
```

**설명**: 에이전트에게 메시지를 전송하고 실시간 스트리밍으로 응답을 받습니다. 메시지는 자동으로 데이터베이스에 저장됩니다.

**인증**: 필수 (access_token 쿠키)

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "항공기 경량화 소재 특허를 찾아줘",
  "session_id": 1
}
```

**Request 필드 설명**:
- `message` (string, 필수): 사용자가 보낼 메시지 내용
- `session_id` (integer, 필수): 대화를 진행할 스레드 ID

**Response**:
- Content-Type: `text/plain`
- 스트리밍 응답 (Server-Sent Events 형식 아님, 단순 텍스트 스트림)
- 에이전트의 응답이 실시간으로 청크 단위로 전송됨

**사용 예시 (Frontend)**:
```typescript
const response = await fetch('/api/v1/chat', {
  method: 'POST',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: '항공기 경량화 소재 특허를 찾아줘',
    session_id: 1
  })
})

const reader = response.body.getReader()
const decoder = new TextDecoder()

while (true) {
  const { done, value } = await reader.read()
  if (done) break
  
  const chunk = decoder.decode(value, { stream: true })
  console.log(chunk) // 실시간으로 텍스트 출력
}
```

---

### 5. 에이전트 (Agent) - `/api/v1/agent`

#### 5.1 에이전트 대화 (비스트리밍)

```
POST /api/v1/agent/chat
```

**설명**: 에이전트와 일반 대화를 나눕니다. 스트리밍이 아닌 완전한 응답을 받습니다. 대화 히스토리를 포함할 수 있습니다.

**인증**: 필수 (access_token 쿠키)

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "항공기 소재 특허를 찾아줘",
  "llm_type": "openai",
  "history": [
    ["user", "안녕하세요"],
    ["assistant", "안녕하세요! 무엇을 도와드릴까요?"]
  ]
}
```

**Request 필드 설명**:
- `query` (string, 필수): 사용자 질문
- `llm_type` (string, 선택, 기본값: "openai"): 사용할 LLM 타입
  - 가능한 값: `"openai"` 또는 `"ollama"`
- `history` (array, 선택): 이전 대화 기록
  - 형식: `[["role", "content"], ...]`
  - role: `"user"`, `"assistant"`, `"system"` 중 하나

**Response Body**:
```json
{
  "response": "항공기 소재와 관련된 특허를 검색한 결과입니다..."
}
```

**Response 필드 설명**:
- `response` (string): 에이전트의 완전한 응답 텍스트

**에러 응답**:
```json
{
  "detail": "에러 메시지"
}
```
Status Code: `500`

---

## 공통 에러 응답

### 인증 실패
```json
{
  "detail": "Unauthorized"
}
```
Status Code: `401`

### 리소스 없음
```json
{
  "detail": "Not found"
}
```
Status Code: `404`

### 권한 없음
```json
{
  "detail": "Forbidden"
}
```
Status Code: `403`

### 서버 오류
```json
{
  "detail": "Internal server error"
}
```
Status Code: `500`

---

## 데이터 모델 (Schemas)

### Thread (스레드)
```typescript
interface Thread {
  id: number
  title: string | null
  user_id: number
  created_at: string  // ISO 8601 형식
}
```

### Message (메시지)
```typescript
interface Message {
  id: number
  content: string
  role: "user" | "assistant"
  created_at: string  // ISO 8601 형식
}
```

### User (사용자)
```typescript
interface User {
  id: number
  email: string
  display_name: string
  profile_image: string
  created_at: string  // ISO 8601 형식
}
```

---

## 개발 시 주의사항

1. **쿠키 인증**: 모든 API 요청 시 `credentials: 'include'` 옵션을 사용하여 쿠키를 포함해야 합니다.

2. **CORS**: Backend가 Frontend의 도메인을 허용하도록 CORS가 설정되어 있습니다.

3. **스트리밍 응답**: `/api/v1/chat` 엔드포인트는 스트리밍 응답을 반환하므로, `ReadableStream`을 사용하여 처리해야 합니다.

4. **에러 처리**: 모든 API는 실패 시 JSON 형식의 에러를 반환하므로, `response.ok`를 확인하고 적절히 처리해야 합니다.

5. **날짜 형식**: 모든 날짜는 ISO 8601 형식의 문자열로 반환됩니다 (예: `"2024-01-01T10:00:00"`).

6. **새 스레드 생성 시점**: 사용자가 첫 메시지를 보낼 때 스레드가 없으면 `/api/v1/threads/create`를 먼저 호출하여 스레드를 생성한 후 `/api/v1/chat`으로 메시지를 전송해야 합니다.
