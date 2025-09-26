from pydantic_settings import BaseSettings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DATABASE: str

    CPU: int = 10
    MEMORY: int = 10
    GPU: int = 2

    CPU_COST: float = 1 / 3600
    MEMORY_COST: float = 0.5 / 3600
    GPU_COST: float = 5 / 3600


    class Config:
        env_file = ".env"

settings = Settings()