"""
Contract tests for common error handling and response format.
Verification IDs: C-019, C-020, S-006, S-007, S-008
"""
import uuid
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.config.database import get_session


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


# ── C-019: Error responses follow { "error": "...", "message": "..." } format ──


@pytest.mark.anyio
async def test_error_response_format_404(app):
    """C-019: 404 error response has exactly error and message fields."""
    from src.domain.exceptions import ProjectNotFound

    fake_id = uuid.uuid4()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.projects.GetProject.execute",
            AsyncMock(side_effect=ProjectNotFound(project_id=fake_id)),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{fake_id}")

    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert "message" in body
    assert isinstance(body["error"], str)
    assert isinstance(body["message"], str)


@pytest.mark.anyio
async def test_error_response_format_422(app):
    """C-019: 422 error response has exactly error and message fields."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/projects/not-a-uuid")

    assert response.status_code == 422
    body = response.json()
    assert "error" in body
    assert "message" in body
    assert isinstance(body["error"], str)
    assert isinstance(body["message"], str)


@pytest.mark.anyio
async def test_error_response_format_409(app):
    """C-019: 409 error response has exactly error and message fields."""
    from src.domain.exceptions import NotYetGenerated

    fake_id = uuid.uuid4()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.download.DownloadProject.execute",
            AsyncMock(side_effect=NotYetGenerated(project_id=fake_id)),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{fake_id}/download")

    assert response.status_code == 409
    body = response.json()
    assert "error" in body
    assert "message" in body
    assert isinstance(body["error"], str)
    assert isinstance(body["message"], str)


# ── C-020: Success responses follow { "data": { ... } } format ──


@pytest.mark.anyio
async def test_success_response_format_intakes(app):
    """C-020: POST /intakes success response wraps result in 'data' key."""
    with pytest.MonkeyPatch.context() as mp:
        from datetime import datetime, timezone

        from src.domain.entities.project import Project

        fake_project = Project(
            id=uuid.uuid4(),
            project_name="test",
            status="intake_saved",
            intake_data={"project": {"name": "test"}},
            zip_path=None,
            created_at=datetime.now(timezone.utc),
            generated_at=None,
        )
        mp.setattr(
            "src.adapters.api.intakes.CreateIntake.execute",
            AsyncMock(return_value=fake_project),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/intakes",
                json={"intake_data": {"project": {"name": "test"}}},
            )

    assert response.status_code == 201
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], dict)


@pytest.mark.anyio
async def test_success_response_format_get_project(app):
    """C-020: GET /projects/:id success response wraps result in 'data' key."""
    from datetime import datetime, timezone

    from src.domain.entities.project import Project

    fake_id = uuid.uuid4()
    fake_project = Project(
        id=fake_id,
        project_name="test",
        status="intake_saved",
        intake_data={"project": {"name": "test"}},
        zip_path=None,
        created_at=datetime.now(timezone.utc),
        generated_at=None,
    )
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.projects.GetProject.execute",
            AsyncMock(return_value=fake_project),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/projects/{fake_id}")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], dict)


@pytest.mark.anyio
async def test_success_response_format_generate(app):
    """C-020: POST /generate success response wraps result in 'data' key."""
    from datetime import datetime, timezone

    from src.domain.entities.project import Project

    fake_id = uuid.uuid4()
    fake_project = Project(
        id=fake_id,
        project_name="test",
        status="generated",
        intake_data={},
        zip_path="/output/test.zip",
        created_at=datetime.now(timezone.utc),
        generated_at=datetime.now(timezone.utc),
    )
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.generate.GenerateDocuments.execute",
            AsyncMock(return_value=fake_project),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/generate",
                json={"project_id": str(fake_id)},
            )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], dict)


# ── S-006: No stack trace in error responses ──


@pytest.mark.anyio
async def test_no_stack_trace_in_unhandled_error(app):
    """S-006: Unhandled exception must not expose stack trace."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.projects.GetProject.execute",
            AsyncMock(side_effect=RuntimeError("something broke internally")),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            fake_id = str(uuid.uuid4())
            response = await client.get(f"/projects/{fake_id}")

    assert response.status_code == 500
    body = response.json()
    assert "error" in body
    assert "message" in body
    # Must not contain Python traceback keywords
    response_text = str(body)
    assert "Traceback" not in response_text
    assert "File " not in response_text
    assert "line " not in response_text


# ── S-007: No DB connection info in error responses ──


@pytest.mark.anyio
async def test_no_db_credentials_in_error(app):
    """S-007: Database exception must not leak connection strings."""
    db_error = Exception("connection to server at 'localhost' (127.0.0.1), port 5432 failed: password authentication failed for user 'admin'")
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.projects.GetProject.execute",
            AsyncMock(side_effect=db_error),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            fake_id = str(uuid.uuid4())
            response = await client.get(f"/projects/{fake_id}")

    assert response.status_code == 500
    body = response.json()
    response_text = str(body).lower()
    assert "password" not in response_text
    assert "localhost" not in response_text
    assert "5432" not in response_text
    assert "admin" not in response_text


# ── S-008: No server info in response headers ──


@pytest.mark.anyio
async def test_no_server_version_in_headers(app):
    """S-008: Response headers must not expose server software version."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/nonexistent-endpoint")

    # Server header should not contain version info
    server_header = response.headers.get("server", "")
    assert "uvicorn" not in server_header.lower()
    assert "fastapi" not in server_header.lower()
    assert "python" not in server_header.lower()
    # Response body should also not expose server details
    body_text = response.text.lower()
    assert "uvicorn" not in body_text
    assert "fastapi" not in body_text
