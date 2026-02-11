from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import AlreadyGenerated, DomainException, NotYetGenerated, ProjectNotFound


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Handle domain exceptions and map them to appropriate HTTP responses."""
    if isinstance(exc, ProjectNotFound):
        return JSONResponse(
            status_code=404,
            content={"error": "PROJECT_NOT_FOUND", "message": str(exc)},
        )
    elif isinstance(exc, AlreadyGenerated):
        return JSONResponse(
            status_code=409,
            content={"error": "ALREADY_GENERATED", "message": str(exc)},
        )
    elif isinstance(exc, NotYetGenerated):
        return JSONResponse(
            status_code=409,
            content={"error": "NOT_YET_GENERATED", "message": str(exc)},
        )
    # Fallback for any other DomainException
    return JSONResponse(
        status_code=500,
        content={"error": "DOMAIN_ERROR", "message": str(exc)},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all unhandled exceptions and return a safe generic error response."""
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "Internal server error"},
    )
