from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.message import ChatRequest
from app.services.message_service import MessageService
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
    
    return StreamingResponse(
        sse_generator(message_stream),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
