from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    
    # Database Settings (PostgreSQL / SQLite fallback)
    DATABASE_URL: str = "sqlite:///./news_aggregator.db"
    
    # ChromaDB Vector Store Settings
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # Security / Auth Settings
    JWT_SECRET: str = "c8f5e29a4b7d16038e12f0c9751e3a649b802e5f1d7a3c9e624b80f1e5d7c3a9"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # LLM Settings
    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Email Settings
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = ""
    EMAIL_APP_PASSWORD: str = ""
    RECIPIENT_EMAIL: str = ""
    
    # Search API Settings (Google Custom Search + Brave Search)
    GOOGLE_CSE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""
    BRAVE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

