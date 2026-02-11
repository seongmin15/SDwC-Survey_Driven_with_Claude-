import uuid
from datetime import datetime, timezone

from src.domain.entities.event import Event
from src.domain.entities.project import Project
from src.domain.ports.repositories import EventRepository, ProjectRepository


class CreateIntake:
    def __init__(
        self,
        project_repo: ProjectRepository,
        event_repo: EventRepository,
    ) -> None:
        self._project_repo = project_repo
        self._event_repo = event_repo

    async def execute(self, intake_data: dict) -> Project:
        project_name = intake_data["project"]["name"]
        now = datetime.now(timezone.utc)

        project = Project(
            id=uuid.uuid4(),
            project_name=project_name,
            status="intake_saved",
            intake_data=intake_data,
            zip_path=None,
            created_at=now,
            generated_at=None,
        )
        created_project = await self._project_repo.create(project)

        event = Event(
            id=uuid.uuid4(),
            project_id=created_project.id,
            event_type="intake_saved",
            payload=None,
            created_at=now,
        )
        await self._event_repo.create(event)

        return created_project
