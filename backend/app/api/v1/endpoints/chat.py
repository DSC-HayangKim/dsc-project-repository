from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.message import ChatRequest
from app.services.message_service import MessageService
from app.api.deps import get_current_user_payload

router = APIRouter()

@router.post("/")
async def chat(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_payload)
):
    """
    사용자 메시지를 받아 에이전트와 대화하고 응답을 스트리밍합니다.
    메시지는 데이터베이스에 저장됩니다.
    """
    return StreamingResponse(
        MessageService.process_chat(session_id=request.session_id,
                                   user_message=request.message),
        media_type="text/plain"
    )
