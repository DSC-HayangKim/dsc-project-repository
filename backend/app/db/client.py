from supabase import create_client, Client
from app.core import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)
