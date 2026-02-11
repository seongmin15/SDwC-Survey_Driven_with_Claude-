"""
Contract tests for GET /projects/:id.
Verification IDs: C-012, C-013, C-014
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.config.database import get_session
from src.domain.entities.project import Project

FAKE_PROJECT_ID = uuid.uuid4()

FAKE_PROJECT = Project(
    id=FAKE_PROJECT_ID,
    project_name="test-app",
    status="intake_saved",
    intake_data={"project": {"name": "test-app"}},
    zip_path=None,
    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    generated_at=None,
)


@pytest.fixture
def mock_session():
    session = AsyncMock()
    return session


@pytest.fixture
def app(mock_session):
    from src.config.app import create_app

    app = create_app()
    app.dependency_overrides[get_session] = lambda: mock_session
    yield app
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_existing_project_returns_200(app):
    """C-012: 존재하는 project_id → 200 OK, 프로젝트 메타 반환"""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.projects.GetProject.execute",
            AsyncMock(return_value=FAKE_PROJECT),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{FAKE_PROJECT_ID}")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    data = body["data"]
    assert data["project_id"] == str(FAKE_PROJECT_ID)
    assert data["project_name"] == "test-app"
    assert data["status"] == "intake_saved"
    assert data["intake_data"] == {"project": {"name": "test-app"}}
    assert "created_at" in data
    assert data["generated_at"] is None


@pytest.mark.anyio
async def test_nonexistent_project_returns_404(app):
    """C-013: 존재하지 않는 project_id → 404"""
    fake_id = str(uuid.uuid4())
    with pytest.MonkeyPatch.context() as mp:
        from src.domain.exceptions import ProjectNotFound

        mp.setattr(
            "src.adapters.api.projects.GetProject.execute",
            AsyncMock(side_effect=ProjectNotFound(project_id=uuid.UUID(fake_id))),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{fake_id}")

    assert response.status_code == 404
    assert response.json()["error"] == "PROJECT_NOT_FOUND"


@pytest.mark.anyio
async def test_invalid_uuid_returns_422(app):
    """C-014: UUID 형식이 아닌 project_id → 422"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/projects/not-a-uuid")

    assert response.status_code == 422
    assert response.json()["error"] == "INVALID_PROJECT_ID"
