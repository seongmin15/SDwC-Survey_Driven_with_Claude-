from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.config.database import check_connection

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    db_ok = await check_connection()
    if not db_ok:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "reason": "database unavailable"},
        )
    return {"status": "ready"}
