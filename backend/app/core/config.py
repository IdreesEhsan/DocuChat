from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    groq_api_key: str
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "llama3-70b-8192"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()