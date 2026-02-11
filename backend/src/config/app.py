from fastapi import FastAPI

from src.adapters.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="SDwC Backend API", version="0.1.0")
    app.include_router(health_router)
    return app
