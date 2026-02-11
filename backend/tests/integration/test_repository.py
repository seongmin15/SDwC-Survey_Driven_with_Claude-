"""
Integration tests for Repository Adapters.
Verification IDs: I-003, I-004, I-005
"""
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from src.domain.entities.event import Event
from src.domain.entities.project import Project


@pytest.fixture
async def db_session(app_with_db):
    """Provide a clean AsyncSession for each test, with rollback."""
    from src.config.database import _session_factory

    async with _session_factory() as session:
        # Clean tables before each test
        await session.execute(text("DELETE FROM events"))
        await session.execute(text("DELETE FROM projects"))
        await session.commit()
        yield session


@pytest.fixture
def sample_project() -> Project:
    return Project(
        id=uuid.uuid4(),
        project_name="test-project",
        status="intake_saved",
        intake_data={
            "project": {"name": "test-project", "type": "web"},
            "tech_stack": {"backend": "python", "frontend": "react"},
        },
        zip_path=None,
        created_at=datetime.now(timezone.utc),
        generated_at=None,
    )


@pytest.fixture
def sample_event(sample_project) -> Event:
    return Event(
        id=uuid.uuid4(),
        project_id=sample_project.id,
        event_type="intake_saved",
        payload={"source": "survey"},
        created_at=datetime.now(timezone.utc),
    )


class TestProjectRepository:
    """I-003: 설문 저장 후 projects 테이블 레코드 존재"""

    @pytest.mark.anyio
    async def test_create_project_persists_record(self, db_session, sample_project):
        """I-003: create 후 projects 테이블에 레코드가 존재한다."""
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository

        repo = SqlAlchemyProjectRepository(db_session)
        created = await repo.create(sample_project)

        assert created.id == sample_project.id
        assert created.project_name == "test-project"

        # Verify in DB directly
        result = await db_session.execute(
            text("SELECT id, project_name, status FROM projects WHERE id = :id"),
            {"id": sample_project.id},
        )
        row = result.one()
        assert row.project_name == "test-project"
        assert row.status == "intake_saved"

    @pytest.mark.anyio
    async def test_get_by_id_returns_project(self, db_session, sample_project):
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository

        repo = SqlAlchemyProjectRepository(db_session)
        await repo.create(sample_project)

        found = await repo.get_by_id(sample_project.id)
        assert found is not None
        assert found.id == sample_project.id
        assert found.project_name == "test-project"

    @pytest.mark.anyio
    async def test_get_by_id_returns_none_for_missing(self, db_session):
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository

        repo = SqlAlchemyProjectRepository(db_session)
        found = await repo.get_by_id(uuid.uuid4())
        assert found is None

    @pytest.mark.anyio
    async def test_update_status(self, db_session, sample_project):
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository

        repo = SqlAlchemyProjectRepository(db_session)
        await repo.create(sample_project)

        updated = await repo.update_status(
            sample_project.id,
            "generated",
            zip_path="/output/test.zip",
            generated_at=datetime.now(timezone.utc),
        )
        assert updated.status == "generated"
        assert updated.zip_path == "/output/test.zip"
        assert updated.generated_at is not None

    @pytest.mark.anyio
    async def test_intake_data_jsonb_stored_accurately(self, db_session, sample_project):
        """I-005: intake_data JSONB가 정확히 저장된다."""
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository

        repo = SqlAlchemyProjectRepository(db_session)
        await repo.create(sample_project)

        found = await repo.get_by_id(sample_project.id)
        assert found.intake_data == sample_project.intake_data
        assert found.intake_data["project"]["name"] == "test-project"
        assert found.intake_data["tech_stack"]["backend"] == "python"


class TestEventRepository:
    """I-004: 설문 저장 후 events 테이블 이벤트 존재"""

    @pytest.mark.anyio
    async def test_create_event_persists_record(self, db_session, sample_project, sample_event):
        """I-004: create 후 events 테이블에 이벤트가 존재한다."""
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
        from src.adapters.persistence.event_repository import SqlAlchemyEventRepository

        # Project must exist first (FK constraint)
        project_repo = SqlAlchemyProjectRepository(db_session)
        await project_repo.create(sample_project)

        event_repo = SqlAlchemyEventRepository(db_session)
        created = await event_repo.create(sample_event)

        assert created.id == sample_event.id
        assert created.event_type == "intake_saved"

        # Verify in DB directly
        result = await db_session.execute(
            text("SELECT id, event_type FROM events WHERE project_id = :pid"),
            {"pid": sample_project.id},
        )
        row = result.one()
        assert row.event_type == "intake_saved"

    @pytest.mark.anyio
    async def test_list_by_project_id(self, db_session, sample_project):
        from src.adapters.persistence.project_repository import SqlAlchemyProjectRepository
        from src.adapters.persistence.event_repository import SqlAlchemyEventRepository

        project_repo = SqlAlchemyProjectRepository(db_session)
        await project_repo.create(sample_project)

        event_repo = SqlAlchemyEventRepository(db_session)
        for etype in ["intake_saved", "generated"]:
            event = Event(
                id=uuid.uuid4(),
                project_id=sample_project.id,
                event_type=etype,
                payload=None,
                created_at=datetime.now(timezone.utc),
            )
            await event_repo.create(event)

        events = await event_repo.list_by_project_id(sample_project.id)
        assert len(events) == 2
        types = {e.event_type for e in events}
        assert types == {"intake_saved", "generated"}

    @pytest.mark.anyio
    async def test_list_by_project_id_empty(self, db_session):
        from src.adapters.persistence.event_repository import SqlAlchemyEventRepository

        event_repo = SqlAlchemyEventRepository(db_session)
        events = await event_repo.list_by_project_id(uuid.uuid4())
        assert events == []
