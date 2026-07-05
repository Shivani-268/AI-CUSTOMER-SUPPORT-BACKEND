import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379").strip()

settings = Settings()