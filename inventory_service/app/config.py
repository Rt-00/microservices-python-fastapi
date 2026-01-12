from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://inventory_user:inventory_pass@inventory_db:5432/inventory_db"
    )
    rabbitmq_url: str = "amqp://admin:admin@rabbitmq:5672/"
    service_name: str = "inventory"

    class Config:
        env_file = ".env"


settings = Settings()
