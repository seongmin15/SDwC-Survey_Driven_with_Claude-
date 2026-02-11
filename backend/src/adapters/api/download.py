from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
from src.application.usecases.download_project import DownloadProject
from src.config.database import get_session
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

    project_repo = SqlAlchemyProjectRepository(session)
    use_case = DownloadProject(project_repo)
    project = await use_case.execute(pid)

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
