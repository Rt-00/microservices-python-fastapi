from contextlib import asynccontextmanager
from fastapi import FastAPI

from .services.messaging import messaging_service
from .database import init_db
from .routes import orders
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    await messaging_service.connect()
    yield

    # Shutdown
    await messaging_service.disconnect()


app = FastAPI(title="Orders Service", version="1.0.0", lifespan=lifespan)

app.include_router(orders.router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.service_name}
