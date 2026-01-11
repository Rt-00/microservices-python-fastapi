from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import init_db
from .routes import orders
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Orders Service", version="1.0.0", lifespan=lifespan)

app.include_router(orders.router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.service_name}
