from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    thread_id: int

class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: int
