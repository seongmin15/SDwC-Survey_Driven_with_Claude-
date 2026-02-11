import uuid

from src.domain.entities.project import Project
from src.domain.exceptions import ProjectNotFound
from src.domain.ports.repositories import ProjectRepository


class GetProject:
    def __init__(self, project_repo: ProjectRepository) -> None:
        self._project_repo = project_repo

    async def execute(self, project_id: uuid.UUID) -> Project:
        project = await self._project_repo.get_by_id(project_id)
        if project is None:
            raise ProjectNotFound(project_id=project_id)
        return project
