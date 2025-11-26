from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.core import process_message_non_streaming

router = APIRouter()

# class TestAskRequest(BaseModel):
#     input_string: str

# @router.post("/test/ask")
# async def test_ask_endpoint(
#     request_body: TestAskRequest
# ) -> str:
#     """
#     문자열을 받아 간단한 함수를 호출하고 결과를 반환하는 테스트 API.
    
#     Args:
#         request_body (TestAskRequest): 처리할 문자열이 포함된 요청 객체.
        
#     Returns:
#         str: 처리된 문자열.
#     """
#     processed_result = await process_message_non_streaming(message=request_body.input_string, history=[])
#     return str(processed_result)