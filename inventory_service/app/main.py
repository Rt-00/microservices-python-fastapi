from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import init_db
from .config import settings
from .routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Inventory Service", version="1.0.0", lifespan=lifespan)

app.include_router(products.router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.service_name}
