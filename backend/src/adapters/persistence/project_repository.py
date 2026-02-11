from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.models import ProjectModel
from src.domain.entities.project import Project
from src.domain.ports.repositories import ProjectRepository


class SqlAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            project_name=model.project_name,
            status=model.status,
            intake_data=model.intake_data,
            zip_path=model.zip_path,
            created_at=model.created_at,
            generated_at=model.generated_at,
        )

    async def create(self, project: Project) -> Project:
        model = ProjectModel(
            id=project.id,
            project_name=project.project_name,
            status=project.status,
            intake_data=project.intake_data,
            zip_path=project.zip_path,
            generated_at=project.generated_at,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, project_id: UUID) -> Project | None:
        result = await self._session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_entity(model)

    async def update_status(
        self, project_id: UUID, status: str, **kwargs: object
    ) -> Project:
        result = await self._session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalar_one()
        model.status = status
        for key, value in kwargs.items():
            setattr(model, key, value)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)
