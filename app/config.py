from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DATABASE: str

    class Config:
        env_file = ".env"

settings = Settings()