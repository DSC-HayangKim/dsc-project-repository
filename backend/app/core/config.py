from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_API_KEY: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env.prod", env_ignore_empty=True)