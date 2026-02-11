from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
from src.application.usecases.get_project import GetProject
from src.config.database import get_session
from src.domain.exceptions import ProjectNotFound

router = APIRouter()


@router.get("/projects/{project_id}")
async def get_project(project_id: str, session: AsyncSession = Depends(get_session)):
    try:
        pid = UUID(project_id)
    except (ValueError, AttributeError):
        return JSONResponse(
            status_code=422,
            content={"error": "INVALID_PROJECT_ID", "message": "project_id must be a valid UUID"},
        )

    try:
        project_repo = SqlAlchemyProjectRepository(session)
        use_case = GetProject(project_repo)
        project = await use_case.execute(pid)
    except ProjectNotFound:
        return JSONResponse(
            status_code=404,
            content={"error": "PROJECT_NOT_FOUND", "message": f"Project not found: {project_id}"},
        )

    return JSONResponse(
        status_code=200,
        content={
            "data": {
                "project_id": str(project.id),
                "project_name": project.project_name,
                "status": project.status,
                "intake_data": project.intake_data,
                "created_at": project.created_at.isoformat() if project.created_at else None,
                "generated_at": project.generated_at.isoformat() if project.generated_at else None,
            }
        },
    )
