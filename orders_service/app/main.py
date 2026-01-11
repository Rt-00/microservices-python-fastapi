from fastapi import FastAPI

app = FastAPI(
    title="Orders Service",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
