from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


class Database:
    client: AsyncIOMotorClient


database = Database()


async def get_database():
    return database.client[settings.database_name]


async def connect_to_mongo():
    """Conectar ao MongoDB"""
    database.client = AsyncIOMotorClient(settings.mongodb_url)
    print("Connected to MongoDB")


async def close_mongo_connection():
    """Fechar conexão com MongoDB"""
    if database.client:
        database.client.close()
        print("Closed MongoDB connection")
