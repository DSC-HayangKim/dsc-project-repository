import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from app.agent.tools.vector_db import vector_db_search

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
        return ChatOpenAI(model="gpt-4o", temperature=0)
    elif llm_type == "ollama":
        # Ollama 서버 URL은 환경 변수 또는 기본값 사용
        return ChatOllama(model="llama3", temperature=0)
    else:
        raise ValueError(f"지원하지 않는 LLM 타입입니다: {llm_type}")

def create_agent_executor(llm_type: str = "openai") -> AgentExecutor:
    """
    주어진 LLM 타입으로 에이전트 실행기(AgentExecutor)를 생성합니다.
    LLM과 도구(Tools)를 바인딩하고 프롬프트를 설정하여 에이전트를 초기화합니다.
    
    Args:
        llm_type (str): 사용할 LLM 타입 (기본값: "openai").
        
    Returns:
        AgentExecutor: 실행 가능한 에이전트 실행기 객체.
    """
    llm = get_llm(llm_type)
    tools = [vector_db_search]
    
    # 간단한 프롬프트 템플릿 정의
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 유용한 AI 어시스턴트입니다. 질문에 답하기 위해 필요한 도구를 사용하세요."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
