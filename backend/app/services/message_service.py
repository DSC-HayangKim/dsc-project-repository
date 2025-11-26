from app.schemas.message import MessageCreate
from app.agent.core import process_message, process_message_non_streaming, generate_thread_title
from app.db.client import supabase
from app.services.thread_service import ThreadService

class MessageService:
    @staticmethod
    async def save_message(message_data: MessageCreate):
        """
        메시지를 데이터베이스에 저장합니다.
        
        Args:
            message_data (MessageCreate): 저장할 메시지 데이터
            
        Returns:
            dict: 저장된 메시지 객체 또는 None
        """
        data = {
            "thread_id": message_data.thread_id,
            "content": message_data.content,
            "role": message_data.role
        }

        # 스레드에 메시지가 없는 경우 (첫 메시지), 제목 생성 및 업데이트
        # 주의: user 메시지일 때만 제목을 생성하도록 조건 추가 가능
        if message_data.role == "user" and not await MessageService.is_exists_any_message(message_data.thread_id):
            try:
                # 제목 생성
                new_title = await generate_thread_title(message_data.content)
                # 제목 업데이트
                await ThreadService.rename_title(message_data.thread_id, new_title)
            except Exception as e:
                print(f"[ERROR] Failed to generate/update thread title: {e}")

        response = supabase.table("messages").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    async def process_chat(session_id: int, user_message: str):
        response = await MessageService.get_messages_by_thread_id(session_id)
        history = [(msg["role"], msg["content"]) for msg in response] if response else []
        
        # 1. Save User Message
        await MessageService.save_message(MessageCreate(
            thread_id=session_id,
            content=user_message,
            role="user"
        ))

        # 2. Stream Agent Response
        full_response = ""
        async for chunk in process_message(user_message, history):
            full_response += chunk
            yield chunk

        # 3. Save Agent Message
        await MessageService.save_message(MessageCreate(
            thread_id=session_id,
            content=full_response,
            role="assistant"
        ))
        
        # 4. Send end stream event
        yield {
            "event": "end_stream",
            "data": {
                "message": "Stream completed",
                "total_chars": len(full_response)
            }
        }

    @staticmethod
    async def process_chat_nonstreaming(session_id: int, user_message: str):
        response = await MessageService.get_messages_by_thread_id(session_id)
        history = [(msg["role"], msg["content"]) for msg in response] if response else []

        # 1. Save User Message
        await MessageService.save_message(MessageCreate(
            thread_id=session_id,
            content=user_message,
            role="user"
        ))

        # 2. Get Agent Response (non-streaming)
        agent_response = await process_message_non_streaming(user_message, history)

        print(f"AI 에게 {agent_response}, 응답 받음\n")

        # 3. Save Agent Message
        await MessageService.save_message(MessageCreate(
            thread_id=session_id,
            content=agent_response,
            role="assistant"
        ))

        return agent_response
    
    @staticmethod
    async def get_messages_by_thread_id(thread_id: int):
        """
        특정 스레드의 메시지 목록을 조회합니다.
        
        Args:
            thread_id (int): 조회할 스레드의 ID
            
        Returns:
            List[dict]: 메시지 목록
        """
        response = supabase.table("messages") \
            .select("*") \
            .eq("thread_id", thread_id) \
            .order("created_at", desc=False) \
            .execute()
            
        return response.data
    
    @staticmethod
    async def is_exists_any_message(thread_id: int) -> bool:
        """
        특정 ID의 스레드에 메시지가 있는지 확인합니다.
        
        Args:
            thread_id (int): 조회할 스레드의 ID.
            
        Returns:
            bool: 스레드에 메시지가 있는지 여부.
        """
        response = supabase.table("messages").select("*").eq("thread_id", thread_id).execute()
        return bool(response.data)
