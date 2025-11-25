from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.message import ChatRequest
from app.services.message_service import MessageService
from app.services.thread_service import ThreadService
from app.api.deps import get_current_user_payload
import json

router = APIRouter()

async def sse_generator(message_stream):
    async for chunk in message_stream:
        if isinstance(chunk, dict):
            # 종료 이벤트 처리
            if chunk.get("event") == "end_stream":
                yield f"event: end_stream\ndata: {json.dumps(chunk.get('data', {}))}\n\n"
                return
        else:
            # 일반 텍스트 청크
            yield f"data: {chunk}\n\n"

@router.post("/")
async def chat(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_payload)
):
    """
    사용자 메시지를 받아 에이전트와 대화하고 응답을 SSE 형식으로 스트리밍합니다.
    메시지는 데이터베이스에 저장됩니다.
    
    SSE(Server-Sent Events) 형식으로 응답:
    - Content-Type: text/event-stream
    - 각 청크: "data: {content}\n\n"
    """
    message_stream = MessageService.process_chat(
        session_id=request.session_id,
        user_message=request.message
    )

    if not await ThreadService.check_user_thread(user_id=int(current_user_id), thread_id=request.session_id):
        raise HTTPException(status_code=404, detail="User does not have access to this thread or thread not found")

    return StreamingResponse(
        sse_generator(message_stream),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/non-streaming")
async def chat_nonstreaming(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_payload)
):
    """
    사용자 메시지를 받아 에이전트와 대화하고 응답을 한 번에 반환합니다 (Non-streaming).
    
    Args:
        request (ChatRequest): 사용자 메시지, 스레드 ID가 포함된 요청 객체.
        
    Returns:
        str: 에이전트의 응답 텍스트.
    """
    # user_id가 session을 가지고 있는지 확인하는 로직 (예시)
    # 실제 구현은 SessionService 또는 데이터베이스 조회 로직이 필요합니다.
    # if not await SessionService.check_user_session(user_id=current_user_id, session_id=request.session_id):
    #     raise HTTPException(status_code=404, detail="User does not have access to this session or session not found")

    if not await ThreadService.check_user_thread(user_id=int(current_user_id), thread_id=request.session_id):
        raise HTTPException(status_code=404, detail="User does not have access to this thread or thread not found")

    response_text = await MessageService.process_chat_nonstreaming(
        session_id=request.session_id,
        user_message=request.message
    )
    
    return response_text
