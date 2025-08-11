from pydantic import BaseSettings, AnyUrl
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "YOUR_SECRET_KEY_CHANGE_ME"  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"
    TAVILY_MCP_URL: Optional[AnyUrl]
    FLUX_MCP_URL: Optional[AnyUrl]
    SMITHERY_API_KEY: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    COOKIE_SECURE: bool = False
    

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
