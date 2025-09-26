from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DATABASE: str

    CPU: int = 10
    MEMORY: int = 10
    GPU: int = 2

    class Config:
        env_file = ".env"

settings = Settings()