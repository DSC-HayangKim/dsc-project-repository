from supabase import create_client, Client
from app.core import settings

class UserService:
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)

    async def get_or_create_user(self, email: str, display_name: str, profile_image: str):
        # Check if user exists
        response = self.supabase.table("users").select("*").eq("email", email).execute()
        
        if response.data:
            return response.data[0]
        
        # Create new user if not exists
        user_data = {
            "email": email,
            "display_name": display_name,
            "profile_image": profile_image,
        }
        
        response = self.supabase.table("users").insert(user_data).execute()
        
        if response.data:
            return response.data[0]
        
        return None

    async def get_user_by_id(self, user_id: int):
        response = self.supabase.table("users").select("*").eq("id", user_id).execute()
        
        if response.data:
            return response.data[0]
        
        return None
