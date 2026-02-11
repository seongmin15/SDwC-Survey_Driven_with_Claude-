from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator


class IntakeRequest(BaseModel):
    intake_data: dict[str, Any]

    @field_validator("intake_data")
    @classmethod
    def validate_intake_data(cls, v: Any) -> dict[str, Any]:
        if not isinstance(v, dict):
            raise ValueError("intake_data must be an object")
        if "project" not in v:
            raise ValueError("intake_data.project is required")
        project = v["project"]
        if not isinstance(project, dict) or "name" not in project:
            raise ValueError("intake_data.project.name is required")
        if not isinstance(project["name"], str) or not project["name"].strip():
            raise ValueError("intake_data.project.name must be a non-empty string")
        return v


class IntakeResponseData(BaseModel):
    project_id: UUID
    status: str
    created_at: datetime


class SuccessResponse(BaseModel):
    data: Any


class ErrorResponse(BaseModel):
    error: str
    message: str
