from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.agent.schemas import AgentRequest, AgentResponse
from app.agent.core import create_agent_executor

router = APIRouter()

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    에이전트와 대화합니다.
    사용자의 질문을 받아 적절한 LLM 및 도구를 사용하여 응답을 생성합니다.
    
    Args:
        request (AgentRequest): 사용자 질문, LLM 타입, 대화 기록이 포함된 요청 객체.
        
    Returns:
        AgentResponse: 에이전트의 응답 텍스트.
        
    Raises:
        HTTPException: 에이전트 실행 중 오류 발생 시 500 에러 반환.
    """
    try:
        # History 변환
        chat_history = []
        if request.history:
            for role, content in request.history:
                if role == "user":
                    chat_history.append(HumanMessage(content=content))
                elif role == "assistant":
                    chat_history.append(AIMessage(content=content))
                elif role == "system":
                    chat_history.append(SystemMessage(content=content))

        executor = create_agent_executor(llm_type=request.llm_type)
        result = await executor.ainvoke({
            "input": request.query,
            "chat_history": chat_history
        })
        return AgentResponse(response=result["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
