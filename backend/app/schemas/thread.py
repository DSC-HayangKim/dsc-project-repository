from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Union

# 스레드 기본 스키마
class ThreadBase(BaseModel):
    title: Optional[str] = None
    user_id: int

# 스레드 생성 스키마
class ThreadCreate(ThreadBase):
    pass

# 스레드 응답 스키마
class Thread(ThreadBase):
    id: int
    created_at: datetime
    title : Union[str, None]
    user_id : int

    model_config = ConfigDict(from_attributes=True)
