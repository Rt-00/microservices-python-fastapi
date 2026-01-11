from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://inventory_user:inventory_pass@inventory_db:5432/inventory_db"
    )
    service_name: str = "inventory"

    class Config:
        env_file = ".env"


settings = Settings()
