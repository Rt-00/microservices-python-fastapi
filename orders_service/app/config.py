from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://orders_user:orders_pass@orders_db:5432/orders_db"
    rabbitmq_url: str = "amqp://admin:admin@rabbitmq:5672/"
    service_name: str = "orders"

    class Config:
        env_file = ".env"


settings = Settings()
