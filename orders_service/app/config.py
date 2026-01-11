from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://orders_user:orders_pass@orders_db:5432/orders_db"
    service_name: str = "orders"

    class Config:
        env_file = ".env"


settings = Settings()
