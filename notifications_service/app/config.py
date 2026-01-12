from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    service_name: str = "notifications"

    class Config:
        env_file = ".env"

settings = Settings()