from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.schemas import IntakeRequest
from src.adapters.persistence.event_repository import SqlAlchemyEventRepository
from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
from src.application.usecases.create_intake import CreateIntake
from src.config.database import get_session

router = APIRouter()


@router.post("/intakes", status_code=201)
async def create_intake(request: Request, session: AsyncSession = Depends(get_session)):
    # Check content type
    content_type = request.headers.get("content-type", "")
    if "application/json" not in content_type:
        return JSONResponse(
            status_code=422,
            content={"error": "UNPROCESSABLE_ENTITY", "message": "Content-Type must be application/json"},
        )

    # Parse raw JSON to handle custom error responses
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "MISSING_REQUIRED_FIELD", "message": "Request body must be valid JSON"},
        )

    if not isinstance(body, dict) or "intake_data" not in body:
        return JSONResponse(
            status_code=400,
            content={"error": "MISSING_REQUIRED_FIELD", "message": "intake_data is required"},
        )

    # Validate intake_data
    try:
        validated = IntakeRequest(**body)
    except ValidationError as e:
        first_error = e.errors()[0]
        if "intake_data must be an object" in str(first_error.get("msg", "")):
            return JSONResponse(
                status_code=400,
                content={"error": "INVALID_INTAKE_DATA", "message": "intake_data must be an object"},
            )
        return JSONResponse(
            status_code=400,
            content={"error": "INVALID_INTAKE_DATA", "message": str(first_error.get("msg", "Validation failed"))},
        )

    # Execute use case
    try:
        project_repo = SqlAlchemyProjectRepository(session)
        event_repo = SqlAlchemyEventRepository(session)
        use_case = CreateIntake(project_repo, event_repo)
        project = await use_case.execute(validated.intake_data)
        await session.commit()
    except Exception:
        await session.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": "INTERNAL_ERROR", "message": "Failed to create intake"},
        )

    return JSONResponse(
        status_code=201,
        content={
            "data": {
                "project_id": str(project.id),
                "status": project.status,
                "created_at": project.created_at.isoformat(),
            }
        },
    )
