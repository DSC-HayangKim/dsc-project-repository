from fastapi import APIRouter, HTTPException
from app.agent.schemas import AgentRequest, AgentResponse
from app.agent.core import create_agent_executor

router = APIRouter()

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    에이전트와 대화합니다.
    사용자의 질문을 받아 적절한 LLM 및 도구를 사용하여 응답을 생성합니다.
    
    Args:
        request (AgentRequest): 사용자 질문과 LLM 타입이 포함된 요청 객체.
        
    Returns:
        AgentResponse: 에이전트의 응답 텍스트.
        
    Raises:
        HTTPException: 에이전트 실행 중 오류 발생 시 500 에러 반환.
    """
    try:
        executor = create_agent_executor(llm_type=request.llm_type)
        result = await executor.ainvoke({"input": request.query})
        return AgentResponse(response=result["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
