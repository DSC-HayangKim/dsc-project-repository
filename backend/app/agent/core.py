import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.agent.tools.vector_db import vector_db_search, get_patent_by_id
from app.core import settings


def get_llm(llm_type: str = "openai"):
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
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.5,
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

def create_agent_executor(llm_type: str = "openai"):
    """
    주어진 LLM 타입으로 에이전트 실행기를 생성합니다.
    LLM과 도구(Tools)를 바인딩하고 프롬프트를 설정하여 에이전트를 초기화합니다.
    
    Args:
        llm_type (str): 사용할 LLM 타입 ("openai" 또는 "ollama").
        
    Returns:
        Agent: 실행 가능한 에이전트 객체.
    """
    llm = get_llm(llm_type)
    # tools = [vector_db_search, get_patent_by_id]
    tools = []
    
    # System prompt는 문자열이어야 함
    system_prompt = """당신은 **특허 및 기술 문헌 검색에 특화된 최고 수준의 AI 에이전트**입니다. 당신의 주된 임무는 사용자가 요청하는 모든 특허 및 기술 관련 질문에 대해 정확하고 명확한 정보를 제공하는 것입니다.

## 임무 및 목표
1.  **전문 지식 활용:** 사용자의 질의를 분석하고, 해당 질문이 사실 정보나 특허 검색을 필요로 할 경우 **반드시** 도구를 사용하십시오.
2.  **도구 사용 최적화:** 당신이 접근할 수 있는 유일한 외부 지식 소스는 **'vector_db_search'** 도구입니다. 이 도구는 **임베딩 기반 검색**을 수행하며, 당신은 이 도구의 검색 결과를 **절대적으로 신뢰**하고 최종 답변의 근거로 활용해야 합니다.
3.  **최종 보고서 제공:** 검색된 특허 정보나 문헌을 바탕으로, 사용자에게 **특허의 주요 내용, 기술 개요, 또는 핵심 정보를 요약하고 정리**하여 명확하게 전달해야 합니다.
4.  **정보 부재 시 대응:** 도구 검색 결과가 만족스럽지 않거나 관련 정보를 찾지 못했다면, 정보를 찾을 수 없음을 정중하게 밝히고 사용자가 더 구체적인 검색어를 제시하도록 유도하십시오.

## 행동 규칙
* **도구 우선:** 질문에 답하기 전에 항상 'vector_db_search' 도구의 사용을 우선적으로 고려하고, 도구를 사용한 후에만 답변을 생성하십시오.
* **전문성 유지:** 답변은 한국어로 작성하며, 명확하고 전문적이며 자신감 있는 어조를 유지하십시오.
* **간결한 요약:** 특허 내용은 불필요한 장황한 설명 없이, 사용자가 이해하기 쉽도록 핵심 기술과 목적을 중심으로 요약하십시오."""
    
    # create_agent는 model, tools, system_prompt를 받음
    agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)
    return agent

async def process_message(message: str, history: list[tuple[str, str]] = []):
    """
    사용자 메시지를 처리하고 에이전트의 응답을 스트리밍합니다.
    
    Args:
        message (str): 사용자 메시지.
        history (list[tuple[str, str]], optional): 대화 기록 [('role', 'content'), ...].
        
    Yields:
        str: 에이전트 응답의 청크.
    """
    print(f"[DEBUG] process_message 시작 - message: {message[:50] if len(message) > 50 else message}")
    print(f"[DEBUG] history 길이: {len(history)}")
    
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
        print(f"[DEBUG] chat_history 구성 완료. 총 {len(chat_history)}개 메시지")

        # 3. 에이전트 실행기 생성
        print(f"[DEBUG] 에이전트 실행기 생성 중...")
        agent_executor = create_agent_executor(llm_type="openai")
        print(f"[DEBUG] 에이전트 실행기 생성 완료")

        # 4. 에이전트 실행 및 스트리밍
        print(f"[DEBUG] 에이전트 스트리밍 시작...")
        chunk_count = 0
        event_types = set()
        async for event in agent_executor.astream_events(
            {"messages": chat_history},
            version="v1"
        ):
            kind = event["event"]
            event_types.add(kind)
            
            # 모든 이벤트 타입 출력 (처음 5개만)
            if len(event_types) <= 5:
                print(f"[DEBUG] 이벤트 타입 발견: {kind}")
            
            # 챗 모델에서 생성된 청크를 필터링
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                # 청크에 내용이 있고, 그것이 문자열이면 yield
                if hasattr(chunk, 'content') and isinstance(chunk.content, str):
                    chunk_count += 1
                    if chunk_count <= 3 or chunk_count % 10 == 0:  # 처음 3개와 이후 10개마다만 출력
                        print(f"[DEBUG] Chunk {chunk_count}: {chunk.content[:20] if len(chunk.content) >20 else chunk.content}")
                    yield chunk.content
                elif isinstance(chunk, str):
                    chunk_count += 1
                    if chunk_count <= 3 or chunk_count % 10 == 0:
                        print(f"[DEBUG] Chunk {chunk_count} (str): {chunk[:20] if len(chunk) > 20 else chunk}")
                    yield chunk
        
        print(f"[DEBUG] 발견된 이벤트 타입들: {event_types}")
        print(f"[DEBUG] 스트리밍 완료. 총 {chunk_count}개 청크")
        
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
        
        # 결과에서 최종 응답 추출
        final_response = result.get("output", "응답을 생성할 수 없습니다.")
        return final_response
        
    except Exception as e:
        print(f"[ERROR] process_message_non_streaming 에러: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return "죄송합니다. 에러가 발생했습니다."