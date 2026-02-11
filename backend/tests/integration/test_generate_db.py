"""
Integration tests for POST /generate — ZIP packaging & DB update.
Verification IDs: I-006, I-007, I-008, I-009, I-012
"""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from unittest.mock import patch, MagicMock

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


async def _create_project(client: AsyncClient) -> str:
    """Helper: create a project via POST /intakes and return project_id."""
    response = await client.post("/intakes", json={"intake_data": VALID_INTAKE_DATA})
    assert response.status_code == 201
    return response.json()["data"]["project_id"]


@pytest.mark.anyio
async def test_generate_updates_status_to_generated(app_with_db, db_session):
    """I-006: 문서 생성 후 projects.status가 generated로 변경된다."""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        project_id = await _create_project(client)
        response = await client.post("/generate", json={"project_id": project_id})

    assert response.status_code == 200

    result = await db_session.execute(
        text("SELECT status FROM projects WHERE id = :id"),
        {"id": project_id},
    )
    assert result.scalar() == "generated"


@pytest.mark.anyio
async def test_generate_sets_zip_path(app_with_db, db_session):
    """I-007: 문서 생성 후 projects.zip_path가 설정된다."""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        project_id = await _create_project(client)
        await client.post("/generate", json={"project_id": project_id})

    result = await db_session.execute(
        text("SELECT zip_path FROM projects WHERE id = :id"),
        {"id": project_id},
    )
    zip_path = result.scalar()
    assert zip_path is not None
    assert project_id in zip_path


@pytest.mark.anyio
async def test_generate_sets_generated_at(app_with_db, db_session):
    """I-008: 문서 생성 후 projects.generated_at이 설정된다."""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        project_id = await _create_project(client)
        await client.post("/generate", json={"project_id": project_id})

    result = await db_session.execute(
        text("SELECT generated_at FROM projects WHERE id = :id"),
        {"id": project_id},
    )
    assert result.scalar() is not None


@pytest.mark.anyio
async def test_generate_creates_generated_event(app_with_db, db_session):
    """I-009: 문서 생성 후 events 테이블에 generated 이벤트가 존재한다."""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        project_id = await _create_project(client)
        await client.post("/generate", json={"project_id": project_id})

    result = await db_session.execute(
        text("SELECT event_type FROM events WHERE project_id = :id AND event_type = 'generated'"),
        {"id": project_id},
    )
    assert result.scalar() == "generated"


@pytest.mark.anyio
async def test_generate_rollback_on_zip_failure(app_with_db, db_session):
    """I-012: ZIP 생성 실패 시 status 변경이 롤백된다."""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        project_id = await _create_project(client)

        with patch(
            "src.application.services.zip_packager.ZipPackager.package",
            side_effect=OSError("Simulated ZIP creation failure"),
        ):
            response = await client.post("/generate", json={"project_id": project_id})

    assert response.status_code == 500

    # status must remain intake_saved
    result = await db_session.execute(
        text("SELECT status, zip_path, generated_at FROM projects WHERE id = :id"),
        {"id": project_id},
    )
    row = result.one()
    assert row.status == "intake_saved"
    assert row.zip_path is None
    assert row.generated_at is None
