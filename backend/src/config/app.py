from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.adapters.api.download import router as download_router
from src.adapters.api.exception_handlers import domain_exception_handler, generic_exception_handler
from src.adapters.api.generate import router as generate_router
from src.adapters.api.health import router as health_router
from src.adapters.api.intakes import router as intakes_router
from src.adapters.api.projects import router as projects_router
from src.config.database import dispose_engine, init_engine
from src.config.settings import get_settings
from src.domain.exceptions import DomainException


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    init_engine(settings.POSTGRESQL_URL)
    yield
    await dispose_engine()


async def exception_middleware(request: Request, call_next):
    """Middleware to catch all exceptions and return safe responses."""
    try:
        response = await call_next(request)
        return response
    except DomainException as exc:
        return await domain_exception_handler(request, exc)
    except Exception as exc:
        return await generic_exception_handler(request, exc)


def create_app() -> FastAPI:
    app = FastAPI(title="SDwC Backend API", version="0.1.0", lifespan=lifespan, debug=False)
    app.middleware("http")(exception_middleware)
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    app.include_router(health_router)
    app.include_router(intakes_router)
    app.include_router(generate_router)
    app.include_router(projects_router)
    app.include_router(download_router)
    return app
