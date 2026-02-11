from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class Event:
    id: UUID
    project_id: UUID
    event_type: str
    payload: dict[str, Any] | None
    created_at: datetime
