from contextlib import asynccontextmanager
import time
from fastapi import FastAPI

from .database import init_db
from .config import settings
from .routers import products
from .services.messaging import messaging_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    await messaging_service.connect()
    yield
    await messaging_service.disconnect()


app = FastAPI(title="Inventory Service", version="1.0.0", lifespan=lifespan)

app.include_router(products.router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.service_name}
