from app.schemas.message import MessageCreate
from app.agent.core import process_message
from app.db.client import supabase

class MessageService:
    @staticmethod
    def save_message(message_data: MessageCreate):
        data = {
            "thread_id": message_data.thread_id,
            "content": message_data.content,
            "role": message_data.role
        }
        response = supabase.table("messages").insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    async def process_chat(session_id: int, user_message: str):
        # 1. Save User Message
        MessageService.save_message(MessageCreate(
            thread_id=session_id,
            content=user_message,
            role="user"
        ))

        # 2. Stream Agent Response
        full_response = ""
        async for chunk in process_message(user_message):
            full_response += chunk
            yield chunk

        # 3. Save Agent Message
        MessageService.save_message(MessageCreate(
            thread_id=session_id,
            content=full_response,
            role="assistant"
        ))
