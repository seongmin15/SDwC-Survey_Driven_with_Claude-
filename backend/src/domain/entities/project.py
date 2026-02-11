from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class Project:
    id: UUID
    project_name: str
    status: str
    intake_data: dict[str, Any]
    zip_path: str | None
    created_at: datetime
    generated_at: datetime | None
