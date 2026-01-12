from contextlib import asynccontextmanager
from fastapi import FastAPI

from .config import settings
from .database import connect_to_mongo, close_mongo_connection
from .routers import notifications
from .services.messaging import messaging_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await messaging_service.connect()
    yield
    await messaging_service.disconnect()
    await close_mongo_connection()


app = FastAPI(title="Notifications Service", version="1.0.0", lifespan=lifespan)


app.include_router(notifications.router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.service_name}
