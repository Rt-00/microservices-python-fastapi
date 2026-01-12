from fastapi import FastAPI

from .config import settings


app = FastAPI(
    title="Notifications Service",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.service_name
    }
