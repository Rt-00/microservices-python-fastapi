from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://notif_user:notif_pass@localhost:27017/"
    rabbitmq_url: str = "amqp://admin:admin@rabbitmq:5672/"
    service_name: str = "notifications"
    database_name: str = "notifications_db"

    class Config:
        env_file = ".env"

settings = Settings()