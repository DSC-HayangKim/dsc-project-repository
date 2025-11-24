from app.schemas.message import MessageCreate
from app.agent.core import process_message
from app.db.client import supabase

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

        print(f"AI 에게 {full_response}, 응답 받음\n")

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

