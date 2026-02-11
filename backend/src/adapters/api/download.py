from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
from src.application.usecases.download_project import DownloadProject
from src.config.database import get_session
from src.domain.exceptions import NotYetGenerated, ProjectNotFound

router = APIRouter()


@router.get("/projects/{project_id}/download")
async def download_project(project_id: str, session: AsyncSession = Depends(get_session)):
    try:
        pid = UUID(project_id)
    except (ValueError, AttributeError):
        return JSONResponse(
            status_code=422,
            content={"error": "INVALID_PROJECT_ID", "message": "project_id must be a valid UUID"},
        )

    try:
        project_repo = SqlAlchemyProjectRepository(session)
        use_case = DownloadProject(project_repo)
        project = await use_case.execute(pid)
    except ProjectNotFound:
        return JSONResponse(
            status_code=404,
            content={"error": "PROJECT_NOT_FOUND", "message": f"Project not found: {project_id}"},
        )
    except NotYetGenerated:
        return JSONResponse(
            status_code=409,
            content={"error": "NOT_YET_GENERATED", "message": f"Project not yet generated: {project_id}"},
        )

    zip_path = Path(project.zip_path)
    if not zip_path.exists():
        return JSONResponse(
            status_code=500,
            content={"error": "FILE_NOT_FOUND", "message": "ZIP file not found on disk"},
        )

    filename = f"{project.project_name}.zip"

    def iterfile():
        with open(zip_path, "rb") as f:
            while chunk := f.read(8192):
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
