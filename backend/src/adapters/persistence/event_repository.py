from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.models import EventModel
from src.domain.entities.event import Event
from src.domain.ports.repositories import EventRepository


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: EventModel) -> Event:
        return Event(
            id=model.id,
            project_id=model.project_id,
            event_type=model.event_type,
            payload=model.payload,
            created_at=model.created_at,
        )

    async def create(self, event: Event) -> Event:
        model = EventModel(
            id=event.id,
            project_id=event.project_id,
            event_type=event.event_type,
            payload=event.payload,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def list_by_project_id(self, project_id: UUID) -> list[Event]:
        result = await self._session.execute(
            select(EventModel)
            .where(EventModel.project_id == project_id)
            .order_by(EventModel.created_at)
        )
        return [self._to_entity(m) for m in result.scalars()]
