import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate


class TestMessageService:
    """MessageService 테스트"""
    
    def test_save_message_success(self):
        """메시지 저장 성공 테스트"""
        # Mock Supabase response
        mock_response = Mock()
        mock_response.data = [{"id": 1, "thread_id": 1, "content": "테스트", "role": "user"}]
        
        with patch('app.services.message_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
            
            # Test
            message_data = MessageCreate(thread_id=1, content="테스트", role="user")
            result = MessageService.save_message(message_data)
            
            # Verify
            assert result is not None
            assert result["id"] == 1
            assert result["content"] == "테스트"
            
            # Verify Supabase was called correctly
            mock_supabase.table.assert_called_once_with("messages")
            mock_supabase.table.return_value.insert.assert_called_once()
    
    def test_save_message_failure(self):
        """메시지 저장 실패 테스트"""
        mock_response = Mock()
        mock_response.data = None
        
        with patch('app.services.message_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
            
            message_data = MessageCreate(thread_id=1, content="테스트", role="user")
            result = MessageService.save_message(message_data)
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_get_messages_by_thread_id(self):
        """스레드별 메시지 조회 테스트"""
        mock_messages = [
            {"id": 1, "thread_id": 1, "content": "안녕하세요", "role": "user"},
            {"id": 2, "thread_id": 1, "content": "안녕하세요!", "role": "assistant"}
        ]
        
        mock_response = Mock()
        mock_response.data = mock_messages
        
        with patch('app.services.message_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
            
            result = await MessageService.get_messages_by_thread_id(1)
            
            assert len(result) == 2
            assert result[0]["content"] == "안녕하세요"
            assert result[1]["role"] == "assistant"
    
    @pytest.mark.asyncio
    async def test_process_chat_flow(self):
        """전체 채팅 플로우 테스트"""
        # Mock dependencies
        mock_save_response = Mock()
        mock_save_response.data = [{"id": 1, "thread_id": 1, "content": "테스트", "role": "user"}]
        
        mock_get_response = Mock()
        mock_get_response.data = []
        
        with patch('app.services.message_service.supabase') as mock_supabase, \
             patch('app.services.message_service.process_message') as mock_process:
            
            # Setup mocks
            mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_save_response
            mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_get_response
            
            # Mock AI response
            async def mock_ai_response():
                yield "안녕"
                yield "하세요"
            
            mock_process.return_value = mock_ai_response()
            
            # Test
            chunks = []
            async for chunk in MessageService.process_chat(session_id=1, user_message="안녕"):
                chunks.append(chunk)
            
            # Verify
            assert len(chunks) == 2
            assert "".join(chunks) == "안녕하세요"
            
            # Verify save_message was called twice (user + assistant)
            assert mock_supabase.table.call_count >= 2


class TestMessageServiceIntegration:
    """통합 테스트 - 실제 동작 검증"""
    
    @pytest.mark.skip(reason="실제 DB 연결 필요")
    @pytest.mark.asyncio
    async def test_real_message_save_and_retrieve(self):
        """실제 DB에 메시지 저장 및 조회"""
        # 실제 thread_id 필요
        thread_id = 1
        
        # 메시지 저장
        user_msg = MessageService.save_message(MessageCreate(
            thread_id=thread_id,
            content="테스트 메시지",
            role="user"
        ))
        
        assert user_msg is not None
        
        # 메시지 조회
        messages = await MessageService.get_messages_by_thread_id(thread_id)
        
        assert len(messages) > 0
        assert any(msg["content"] == "테스트 메시지" for msg in messages)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
