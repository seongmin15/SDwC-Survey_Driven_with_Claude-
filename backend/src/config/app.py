from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.api.health import router as health_router
from src.adapters.api.intakes import router as intakes_router
from src.config.database import dispose_engine, init_engine
from src.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    init_engine(settings.POSTGRESQL_URL)
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    app = FastAPI(title="SDwC Backend API", version="0.1.0", lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(intakes_router)
    return app
