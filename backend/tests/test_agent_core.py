import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from app.agent.core import get_llm, create_agent_executor, process_message

class TestGetLLM:
    """LLM 인스턴스 생성 테스트"""
    
    # def test_get_llm_openai(self):
    #     """OpenAI LLM 생성 확인"""
    #     llm = get_llm("openai")
    #     assert isinstance(llm, ChatOpenAI)
    #     assert llm.model_name == "gpt-4o"
    #     assert llm.temperature == 0.5
    
    def test_get_llm_ollama(self):
        """Ollama LLM 생성 확인"""
        llm = get_llm("ollama")
        assert isinstance(llm, ChatOllama)
        assert llm.model == "gpt-oss:20b"
        assert llm.temperature == 0.5
    
    # def test_get_llm_invalid_type(self):
    #     """지원하지 않는 LLM 타입 에러 확인"""
    #     with pytest.raises(ValueError, match="지원하지 않는 LLM 타입"):
    #         get_llm("invalid_type")


class TestCreateAgentExecutor:
    """에이전트 실행기 생성 테스트"""
    
    def test_create_agent_executor_returns_agent(self):
        """에이전트가 정상적으로 생성되는지 확인"""
        agent = create_agent_executor("ollama")
        assert agent is not None
        # Agent should be callable/invokable
        assert hasattr(agent, 'ainvoke') or hasattr(agent, 'astream')


class TestProcessMessage:
    """메시지 처리 및 스트리밍 테스트"""
    
    @pytest.mark.asyncio
    async def test_process_message_without_history(self):
        """히스토리 없이 메시지 처리"""
        # Mock the agent executor
        mock_chunk = {"output": "테스트 응답입니다"}
        
        with patch('app.agent.core.create_agent_executor') as mock_create:
            mock_executor = MagicMock()
            
            async def mock_astream(*args, **kwargs):
                yield mock_chunk
            
            mock_executor.astream = mock_astream
            mock_create.return_value = mock_executor
            
            result = []
            async for chunk in process_message("테스트 질문"):
                result.append(chunk)
            
            assert len(result) == 1
            assert result[0] == "테스트 응답입니다"
    
    @pytest.mark.asyncio
    async def test_process_message_with_history(self):
        """히스토리와 함께 메시지 처리"""
        history = [
            ("user", "안녕하세요"),
            ("assistant", "안녕하세요! 무엇을 도와드릴까요?")
        ]
        
        mock_chunk = {"output": "네, 도와드리겠습니다"}
        
        with patch('app.agent.core.create_agent_executor') as mock_create:
            mock_executor = MagicMock()
            
            async def mock_astream(*args, **kwargs):
                # Verify history was passed
                assert "chat_history" in kwargs or (args and "chat_history" in args[0])
                yield mock_chunk
            
            mock_executor.astream = mock_astream
            mock_create.return_value = mock_executor
            
            result = []
            async for chunk in process_message("도와주세요", history):
                result.append(chunk)
            
            assert len(result) == 1
            assert result[0] == "네, 도와드리겠습니다"


class TestIntegration:
    """통합 테스트 - 실제 AI 호출 (수동 실행용)"""
    
    @pytest.mark.skip(reason="실제 AI를 호출하므로 수동으로만 실행")
    @pytest.mark.asyncio
    async def test_real_agent_execution(self):
        """실제 Ollama/OpenAI 호출 테스트"""
        print("\n🤖 실제 AI 응답 테스트:\n")
        
        full_response = ""
        async for chunk in process_message("안녕하세요"):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print(f"\n\n✅ 응답 완료! (총 {len(full_response)}자)")
        assert len(full_response) > 0
    
    @pytest.mark.skip(reason="벡터 DB 검색 포함하므로 수동으로만 실행")
    @pytest.mark.asyncio
    async def test_vector_db_search_integration(self):
        """벡터 DB 검색 도구를 실제로 호출하는 테스트"""
        print("\n🔍 벡터 DB 검색 테스트:\n")
        
        query = "항공기 소재에 대한 특허"
        
        full_response = ""
        async for chunk in process_message(query):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print(f"\n\n✅ 응답 완료! (총 {len(full_response)}자)")
        
        # 벡터 DB에서 검색한 결과가 포함되어 있어야 함
        assert len(full_response) > 0
