"""
Contract tests for POST /generate.
Verification IDs: C-007, C-008, C-009, C-010, C-011
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.config.database import get_session
from src.domain.entities.project import Project
from src.domain.exceptions import AlreadyGenerated, ProjectNotFound

FAKE_PROJECT_ID = uuid.uuid4()

FAKE_PROJECT = Project(
    id=FAKE_PROJECT_ID,
    project_name="test-app",
    status="generated",
    intake_data={"project": {"name": "test-app"}},
    zip_path="/output/test-app.zip",
    created_at=datetime.now(timezone.utc),
    generated_at=datetime.now(timezone.utc),
)


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def app(mock_session):
    """App with mocked DB session for contract tests."""
    from src.config.app import create_app

    app = create_app()
    app.dependency_overrides[get_session] = lambda: mock_session
    yield app
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_valid_project_id_returns_200(app):
    """C-007: 유효한 project_id (status: intake_saved) → 200 OK, status: generated"""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.generate.GenerateDocuments.execute",
            AsyncMock(return_value=FAKE_PROJECT),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/generate", json={"project_id": str(FAKE_PROJECT_ID)})
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"]["status"] == "generated"
    assert body["data"]["project_id"] == str(FAKE_PROJECT_ID)
    assert "download_url" in body["data"]
    assert "generated_at" in body["data"]


@pytest.mark.anyio
async def test_missing_project_id_returns_400(app):
    """C-008: project_id 누락 → 400"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/generate", json={})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "MISSING_REQUIRED_FIELD"


@pytest.mark.anyio
async def test_nonexistent_project_id_returns_404(app):
    """C-009: 존재하지 않는 project_id → 404"""
    fake_id = str(uuid.uuid4())
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.generate.GenerateDocuments.execute",
            AsyncMock(side_effect=ProjectNotFound(project_id=uuid.UUID(fake_id))),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/generate", json={"project_id": fake_id})
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "PROJECT_NOT_FOUND"


@pytest.mark.anyio
async def test_invalid_uuid_returns_422(app):
    """C-010: UUID 형식이 아닌 project_id → 422"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/generate", json={"project_id": "not-a-uuid"})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "INVALID_PROJECT_ID"


@pytest.mark.anyio
async def test_already_generated_returns_409(app):
    """C-011: 이미 generated 상태 → 409"""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.generate.GenerateDocuments.execute",
            AsyncMock(side_effect=AlreadyGenerated(project_id=FAKE_PROJECT_ID)),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/generate", json={"project_id": str(FAKE_PROJECT_ID)})
    assert response.status_code == 409
    body = response.json()
    assert body["error"] == "ALREADY_GENERATED"
