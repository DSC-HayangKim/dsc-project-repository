from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_API_KEY: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env.prod", env_ignore_empty=True)

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None) -> str:
        if isinstance(v, str) and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://")
        return v