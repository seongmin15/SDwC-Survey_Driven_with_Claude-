"""
Integration test for POST /intakes transaction rollback.
Verification ID: I-011
"""
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from unittest.mock import patch, AsyncMock

VALID_INTAKE_DATA = {
    "project": {"name": "test-app", "description": "A test", "target_users": "devs", "core_value": "testing"},
    "scope": {"in_scope": ["feature A"], "out_of_scope": "none"},
    "architecture": {"pattern": "monolith", "internal_style": "hexagonal"},
    "services": ["backend_api"],
    "backend": {"language": "python", "framework": "fastapi"},
}


@pytest.fixture
async def db_session(app_with_db):
    """Provide a clean DB session for verification."""
    from src.config.database import _session_factory

    async with _session_factory() as session:
        await session.execute(text("DELETE FROM events"))
        await session.execute(text("DELETE FROM projects"))
        await session.commit()
        yield session


@pytest.mark.anyio
async def test_intakes_transaction_rollback_on_event_failure(app_with_db, db_session):
    """I-011: events INSERT 실패 시 projects도 롤백된다."""
    transport = ASGITransport(app=app_with_db)

    with patch(
        "src.adapters.persistence.event_repository.SqlAlchemyEventRepository.create",
        new_callable=AsyncMock,
        side_effect=RuntimeError("Simulated event insert failure"),
    ):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/intakes", json={"intake_data": VALID_INTAKE_DATA})

    assert response.status_code == 500

    # Verify rollback: no projects or events should exist
    proj_count = await db_session.execute(text("SELECT COUNT(*) FROM projects"))
    assert proj_count.scalar() == 0

    evt_count = await db_session.execute(text("SELECT COUNT(*) FROM events"))
    assert evt_count.scalar() == 0
