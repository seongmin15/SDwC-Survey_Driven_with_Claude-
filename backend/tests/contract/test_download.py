"""
Contract tests for GET /projects/:id/download.
Verification IDs: C-015, C-016, C-017, C-018
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.config.database import get_session
from src.domain.entities.project import Project
from src.domain.exceptions import NotYetGenerated, ProjectNotFound

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
    return session


@pytest.fixture
def app(mock_session):
    from src.config.app import create_app

    app = create_app()
    app.dependency_overrides[get_session] = lambda: mock_session
    yield app
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_generated_project_returns_200_zip(app, tmp_path):
    """C-015: generated 상태 프로젝트 → 200, application/zip"""
    # Create a real ZIP file for streaming
    zip_file = tmp_path / "test-app.zip"
    import zipfile, io

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("README.md", "hello")
    zip_file.write_bytes(buf.getvalue())

    project = Project(
        id=FAKE_PROJECT_ID,
        project_name="test-app",
        status="generated",
        intake_data={},
        zip_path=str(zip_file),
        created_at=datetime.now(timezone.utc),
        generated_at=datetime.now(timezone.utc),
    )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.download.DownloadProject.execute",
            AsyncMock(return_value=project),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{FAKE_PROJECT_ID}/download")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert "test-app.zip" in response.headers["content-disposition"]


@pytest.mark.anyio
async def test_nonexistent_project_returns_404(app):
    """C-016: 존재하지 않는 project_id → 404"""
    fake_id = str(uuid.uuid4())
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.download.DownloadProject.execute",
            AsyncMock(side_effect=ProjectNotFound(project_id=uuid.UUID(fake_id))),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{fake_id}/download")

    assert response.status_code == 404
    assert response.json()["error"] == "PROJECT_NOT_FOUND"


@pytest.mark.anyio
async def test_not_yet_generated_returns_409(app):
    """C-017: 아직 generated가 아닌 프로젝트 → 409"""
    fake_id = str(uuid.uuid4())
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.download.DownloadProject.execute",
            AsyncMock(side_effect=NotYetGenerated(project_id=uuid.UUID(fake_id))),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{fake_id}/download")

    assert response.status_code == 409
    assert response.json()["error"] == "NOT_YET_GENERATED"


@pytest.mark.anyio
async def test_invalid_uuid_returns_422(app):
    """C-018: UUID 형식이 아닌 project_id → 422"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/projects/not-a-uuid/download")

    assert response.status_code == 422
    assert response.json()["error"] == "INVALID_PROJECT_ID"
