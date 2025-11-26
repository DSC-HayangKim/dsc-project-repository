from typing import List
from app.db.client import supabase
from app.schemas.thread import Thread

class ThreadService:
    @staticmethod
    async def get_threads(user_id: int, skip: int = 0, limit: int = 100) :
        """
        특정 사용자의 스레드를 생성일 기준 내림차순으로 조회합니다.
        Supabase Client를 직접 사용하여 데이터를 조회합니다.
        
        Args:
            user_id (int): 조회할 사용자의 ID.
            skip (int): 건너뛸 항목 수 (기본값: 0).
            limit (int): 반환할 항목 수 (기본값: 100).
            
        Returns:
            List[Thread]: 조회된 스레드 객체 리스트.
        """
        # Supabase table select
        response = supabase.table("threads") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .range(skip, skip + limit - 1) \
            .execute()

        # Pydantic 모델로 변환
        # Pydantic 모델로 변환하지 않고 dictionary 형태로 반환
        return response.data
        #return [Thread(**item) for item in response.data]

    @staticmethod
    async def create_thread(user_id: int) -> Thread:
        """
        새로운 스레드를 생성합니다.
        
        Args:
            user_id (int): 스레드를 생성할 사용자의 ID.
            
        Returns:
            Thread: 생성된 스레드 객체. 생성 실패 시 None 반환.
        """
        response = supabase.table("threads").insert({"user_id": user_id}).execute()

        if not response.data:
            return None
            
        return Thread(**response.data[0])
    
    async def get_thread_by_id(thread_id: int) -> Thread:
        """
        특정 ID의 스레드를 조회합니다.
        
        Args:
            thread_id (int): 조회할 스레드의 ID.
            
        Returns:
            Thread: 조회된 스레드 객체. 조회 실패 시 None 반환.
        """
        response = supabase.table("threads").select("*").eq("id", thread_id).execute()

        if not response.data:
            return None
            
        return Thread(**response.data[0])
    
    @staticmethod
    async def check_user_thread(user_id: int, thread_id: int) -> bool:
        """
        특정 사용자가 특정 스레드에 대한 접근 권한이 있는지 확인합니다.
        
        Args:
            user_id (int): 사용자의 ID.
            thread_id (int): 스레드의 ID.
            
        Returns:
            bool: 사용자가 스레드에 대한 접근 권한이 있는지 여부.
        """
        response = supabase.table("threads").select("*").eq("user_id", user_id).eq("id", thread_id).execute()
        return bool(response.data)

    @staticmethod
    async def rename_title(thread_id: int, new_title: str) -> bool:
        """
        특정 ID의 스레드의 제목을 변경합니다.
        
        Args:
            thread_id (int): 변경할 스레드의 ID.
            new_title (str): 새로운 제목.
            
        Returns:
            bool: 제목 변경 성공 여부.
        """
        response = supabase.table("threads").update({"title": new_title}).eq("id", thread_id).execute()
        return bool(response.data)
    
