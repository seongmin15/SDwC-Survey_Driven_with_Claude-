import uuid
from datetime import datetime, timezone

from src.application.services.document_generator import DocumentGenerator
from src.application.services.zip_packager import ZipPackager
from src.domain.entities.event import Event
from src.domain.entities.project import Project
from src.domain.exceptions import AlreadyGenerated, ProjectNotFound
from src.domain.ports.repositories import EventRepository, ProjectRepository


class GenerateDocuments:
    def __init__(
        self,
        project_repo: ProjectRepository,
        event_repo: EventRepository,
        zip_packager: ZipPackager,
    ) -> None:
        self._project_repo = project_repo
        self._event_repo = event_repo
        self._generator = DocumentGenerator()
        self._zip_packager = zip_packager

    async def execute(self, project_id: uuid.UUID) -> Project:
        project = await self._project_repo.get_by_id(project_id)
        if project is None:
            raise ProjectNotFound(project_id=project_id)
        if project.status == "generated":
            raise AlreadyGenerated(project_id=project_id)

        # Generate document files from intake_data
        files = self._generator.generate(project.intake_data)

        # Package into ZIP
        zip_path = self._zip_packager.package(project_id, files)

        # Update project status with zip_path and generated_at
        now = datetime.now(timezone.utc)
        updated = await self._project_repo.update_status(
            project_id, "generated", zip_path=zip_path, generated_at=now,
        )

        event = Event(
            id=uuid.uuid4(),
            project_id=project_id,
            event_type="generated",
            payload={"file_count": len(files)},
            created_at=now,
        )
        await self._event_repo.create(event)

        return updated
