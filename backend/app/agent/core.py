import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.agent.tools.vector_db import vector_db_search, get_patent_by_id, get_contact_info_by_applicant, get_patent_by_applicant_number
from app.core import settings


def get_llm(llm_type: str):
    """
    지정된 타입에 따라 LLM 인스턴스를 반환합니다.
    
    Args:
        llm_type (str): 사용할 LLM 타입 ("openai" 또는 "ollama").
        
    Returns:
        BaseChatModel: 구성된 LLM 인스턴스 (ChatOpenAI 또는 ChatOllama).
        
    Raises:
        ValueError: 지원하지 않는 LLM 타입인 경우 발생.
    """
    if llm_type == "openai":
        # API Key는 환경 변수 OPENAI_API_KEY에서 자동으로 로드됩니다.
        return ChatOpenAI(model="gpt-4o", temperature=0.9,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    elif llm_type == "ollama":
        # Ollama 서버 URL은 환경 변수 또는 기본값 사용
        return ChatOllama(
            model="gpt-oss:20b",
            temperature=0.5,
            base_url="http://localhost:11434",
        )
    else:
        raise ValueError(f"지원하지 않는 LLM 타입입니다: {llm_type}")

def create_agent_executor(llm_type: str):
    """
    주어진 LLM 타입으로 에이전트 실행기를 생성합니다.
    LLM과 도구(Tools)를 바인딩하고 프롬프트를 설정하여 에이전트를 초기화합니다.
    
    Args:
        llm_type (str): 사용할 LLM 타입 ("openai" 또는 "ollama").
        
    Returns:
        Agent: 실행 가능한 에이전트 객체.
    """
    llm = get_llm(llm_type)
    tools = [vector_db_search, get_patent_by_id, get_contact_info_by_applicant, get_patent_by_applicant_number]
    
    # System prompt는 문자열이어야 함
    system_prompt = """당신은 **특허 및 기술 문헌 검색에 특화된 최고 수준의 AI 에이전트**입니다. 당신의 주된 임무는 사용자가 요청하는 모든 특허 및 기술 관련 질문에 대해 정확하고 명확한 정보를 제공하는 것입니다.

## 임무 및 목표
1.  **전문 지식 활용:** 사용자의 질의를 분석하고, 해당 질문이 사실 정보나 특허 검색을 필요로 할 경우 **반드시** 도구를 사용하십시오.
2.  **도구 사용 최적화:** 당신이 접근할 수 있는 유일한 외부 지식 소스는 **'vector_db_search'** 도구입니다. 이 도구는 **임베딩 기반 검색**을 수행하며, 당신은 이 도구의 검색 결과를 **절대적으로 신뢰**하고 최종 답변의 근거로 활용해야 합니다.
3.  **최종 보고서 제공:** 검색된 특허 정보나 문헌을 바탕으로, 사용자에게 **특허의 주요 내용, 기술 개요, 또는 핵심 정보를 요약하고 정리**하여 명확하게 전달해야 합니다.
4.  **정보 제공 원칙:** 사용자가 필요로 하지 않을 것 같은 불필요한 정보는 철저히 배제하고, 핵심적이고 요청된 정보만을 제공합니다. 만약 도구 검색 결과가 만족스럽지 않거나 관련 정보를 찾지 못했다면, 정보를 찾을 수 없음을 정중하게 밝히고 사용자가 더 구체적인 검색어를 제시하거나 추가적인 검색을 통해 정보를 얻을 수 있도록 유도하십시오.

## 행동 규칙
* **도구 우선:** 질문에 답하기 전에 항상 'vector_db_search' 도구의 사용을 우선적으로 고려하고, 도구를 사용한 후에만 답변을 생성하십시오.
* **전문성 유지:** 답변은 한국어로 작성하며, 명확하고 전문적이며 자신감 있는 어조를 유지하십시오.
* **간결한 요약:** 특허 내용은 불필요한 장황한 설명 없이, 사용자가 이해하기 쉽도록 핵심 기술과 목적을 중심으로 요약하십시오.
* **연락처 정보:** 특허권자에 대한 컨택정보를 무조건 명시하여 제공하세요. 'get_contact_info_by_applicant' 도구를 사용하여 정확한 정보를 제공하십시오.
* **가독성 및 포맷팅:** 답변은 **Markdown 형식**을 적극적으로 활용하여 가독성을 높이십시오.
    - **헤딩(#, ##)**을 사용하여 문단을 구조화하십시오.
    - **불릿 포인트(-)**나 **번호 매기기(1.)**를 사용하여 항목을 나열하십시오.
    - 중요한 키워드는 **볼드체(**)**로 강조하십시오.
    - 데이터나 비교가 필요한 경우 **테이블**을 사용하십시오.
    - 긴 줄글보다는 짧고 명확한 문장을 사용하십시오.
    - 각 특허들에 대해 잠재적 가치에 대한 점수를 매기고 그 순서대로 출력하세요.
    - 각 특허를 추천한 이유를 상세하게 서술하세요
"""

    
    # create_agent는 model, tools, system_prompt를 받음
    agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)
    return agent

async def generate_thread_title(message: str) -> str:
    """
    사용자 메시지를 기반으로 스레드 제목을 생성합니다.
    
    Args:
        message (str): 사용자 메시지.
        
    Returns:
        str: 생성된 제목 (24자 이내).
    """
    try:
        llm = get_llm("openai")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 특허를 제공하는 전문적인 AI Assitance입니다. 사용자의 질문을 보고 24자 이내의 짧고 명확한 대화 제목을 한국어로 생성해줘. 따옴표 없이 제목만 출력해."),
            ("user", "{message}")
        ])
        chain = prompt | llm
        result = await chain.ainvoke({"message": message})
        return result.content.strip()
    except Exception as e:
        print(f"[ERROR] generate_thread_title 에러: {str(e)}")
        return "새로운 대화"

async def process_message(message: str, history: list[tuple[str, str]] = []):
    """
    사용자 메시지를 처리하고 에이전트의 응답을 스트리밍합니다.
    
    Args:
        message (str): 사용자 메시지.
        history (list[tuple[str, str]], optional): 대화 기록 [('role', 'content'), ...].
        
    Yields:
        str: 에이전트 응답의 청크.
    """
    
    try:
        # 1. History 변환 - 이전 대화 내역
        chat_history = []
        if history:
            for role, content in history:
                if role == "user":
                    chat_history.append(HumanMessage(content=content))
                elif role == "assistant":
                    chat_history.append(AIMessage(content=content))
                elif role == "system":
                    chat_history.append(SystemMessage(content=content))
        
        # 2. 현재 사용자 메시지 추가
        chat_history.append(HumanMessage(content=message))

        # 3. 에이전트 실행기 생성
        agent_executor = create_agent_executor(llm_type="openai")

        # 4. 에이전트 실행 및 스트리밍
        async for event in agent_executor.astream_events(
            {"messages": chat_history},
            version="v1"
        ):
            kind = event["event"]
            
            # 챗 모델에서 생성된 청크를 필터링
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                # 청크에 내용이 있고, 그것이 문자열이면 yield
                if hasattr(chunk, 'content') and isinstance(chunk.content, str):
                    yield chunk.content
                elif isinstance(chunk, str):
                    yield chunk
    except Exception as e:
        print(f"[ERROR] process_message 에러: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        yield "죄송합니다. 에러가 발생했습니다."

async def process_message_non_streaming(message: str, history: list[tuple[str, str]] = []):
    """
    사용자 메시지를 처리하고 에이전트의 응답을 한 번에 반환합니다 (스트리밍 아님).
    
    Args:
        message (str): 사용자 메시지.
        history (list[tuple[str, str]], optional): 대화 기록 [('role', 'content'), ...].
        
    Returns:
        str: 에이전트의 최종 응답.
    """
    try:
        # 1. History 변환 - 이전 대화 내역
        chat_history = []
        if history:
            for role, content in history:
                if role == "user":
                    chat_history.append(HumanMessage(content=content))
                elif role == "assistant":
                    chat_history.append(AIMessage(content=content))
                elif role == "system":
                    chat_history.append(SystemMessage(content=content))
        
        # 2. 현재 사용자 메시지 추가
        chat_history.append(HumanMessage(content=message))

        # 3. 에이전트 실행기 생성
        agent_executor = create_agent_executor(llm_type="openai")

        # 4. 에이전트 실행 및 최종 응답 반환
        result = await agent_executor.ainvoke(
            {"messages": chat_history}
        )

        print(f"[DEBUG] 최종 응답 타입: {type(result)}")
        print(f"[DEBUG] 최종 응답 키: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        # 결과에서 최종 응답 추출
        # LangChain agent는 messages 리스트로 결과를 반환
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            # 마지막 메시지가 AI의 응답
            if messages and len(messages) > 0:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    final_response = last_message.content
                else:
                    final_response = str(last_message)
            else:
                final_response = "응답을 생성할 수 없습니다."
        else:
            final_response = "응답을 생성할 수 없습니다."

        print(f"[DEBUG] 추출된 응답: {final_response[:100] if len(final_response) > 100 else final_response}")
        return final_response
        
    except Exception as e:
        print(f"[ERROR] process_message_non_streaming 에러: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return "죄송합니다. 에러가 발생했습니다."