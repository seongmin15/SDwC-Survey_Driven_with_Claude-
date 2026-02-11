from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.event_repository import SqlAlchemyEventRepository
from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
from src.application.services.zip_packager import ZipPackager
from src.application.usecases.generate_documents import GenerateDocuments
from src.config.database import get_session
from src.config.settings import get_settings
from src.domain.exceptions import AlreadyGenerated, ProjectNotFound

router = APIRouter()


@router.post("/generate")
async def generate(request: Request, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "MISSING_REQUIRED_FIELD", "message": "Request body must be valid JSON"},
        )

    if not isinstance(body, dict) or "project_id" not in body:
        return JSONResponse(
            status_code=400,
            content={"error": "MISSING_REQUIRED_FIELD", "message": "project_id is required"},
        )

    try:
        project_id = UUID(body["project_id"])
    except (ValueError, AttributeError):
        return JSONResponse(
            status_code=422,
            content={"error": "INVALID_PROJECT_ID", "message": "project_id must be a valid UUID"},
        )

    try:
        project_repo = SqlAlchemyProjectRepository(session)
        event_repo = SqlAlchemyEventRepository(session)
        settings = get_settings()
        zip_packager = ZipPackager(settings.OUTPUT_DIR)
        use_case = GenerateDocuments(project_repo, event_repo, zip_packager)
        project = await use_case.execute(project_id)
        await session.commit()
    except ProjectNotFound:
        return JSONResponse(
            status_code=404,
            content={"error": "PROJECT_NOT_FOUND", "message": f"Project not found: {body['project_id']}"},
        )
    except AlreadyGenerated:
        return JSONResponse(
            status_code=409,
            content={"error": "ALREADY_GENERATED", "message": f"Project already generated: {body['project_id']}"},
        )
    except Exception:
        await session.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": "INTERNAL_ERROR", "message": "Failed to generate documents"},
        )

    return JSONResponse(
        status_code=200,
        content={
            "data": {
                "project_id": str(project.id),
                "status": project.status,
                "download_url": f"/projects/{project.id}/download",
                "generated_at": project.generated_at.isoformat() if project.generated_at else None,
            }
        },
    )
