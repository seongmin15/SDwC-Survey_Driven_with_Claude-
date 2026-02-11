"""
Integration test for GET /projects/:id → DB.
Verification ID: I-010
"""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

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
async def test_get_project_matches_db_data(app_with_db, db_session):
    """I-010: 조회 결과가 DB 데이터와 일치한다."""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a project first
        create_resp = await client.post("/intakes", json={"intake_data": VALID_INTAKE_DATA})
        assert create_resp.status_code == 201
        project_id = create_resp.json()["data"]["project_id"]

        # Fetch via GET /projects/:id
        get_resp = await client.get(f"/projects/{project_id}")

    assert get_resp.status_code == 200
    data = get_resp.json()["data"]

    # Verify against DB directly
    result = await db_session.execute(
        text("SELECT project_name, status, intake_data, created_at, generated_at FROM projects WHERE id = :id"),
        {"id": project_id},
    )
    row = result.one()

    assert data["project_id"] == project_id
    assert data["project_name"] == row.project_name
    assert data["status"] == row.status
    assert data["intake_data"] == VALID_INTAKE_DATA
    assert data["generated_at"] is None
