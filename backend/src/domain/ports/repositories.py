from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.event import Event
from src.domain.entities.project import Project


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: Project) -> Project: ...

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Project | None: ...

    @abstractmethod
    async def update_status(
        self, project_id: UUID, status: str, **kwargs: object
    ) -> Project: ...


class EventRepository(ABC):
    @abstractmethod
    async def create(self, event: Event) -> Event: ...

    @abstractmethod
    async def list_by_project_id(self, project_id: UUID) -> list[Event]: ...
