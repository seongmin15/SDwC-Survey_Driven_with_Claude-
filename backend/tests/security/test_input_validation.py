"""
Security tests for input validation.
Verification IDs: S-001, S-002, S-003, S-004, S-005
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.config.database import get_session
from src.domain.entities.project import Project


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def app(mock_session):
    from src.config.app import create_app

    app = create_app()
    app.dependency_overrides[get_session] = lambda: mock_session
    yield app
    app.dependency_overrides.clear()


# ── S-001: SQL injection in intake_data is stored normally (JSONB) ──


@pytest.mark.anyio
async def test_sql_injection_in_intake_data_accepted(app):
    """S-001: SQL injection strings in intake_data are stored normally via JSONB."""
    sql_injection_data = {
        "project": {
            "name": "'; DROP TABLE projects; --",
            "description": "Robert'); DROP TABLE students;--",
        },
        "extra": "1 OR 1=1; SELECT * FROM users",
    }
    fake_project = Project(
        id=uuid.uuid4(),
        project_name="'; DROP TABLE projects; --",
        status="intake_saved",
        intake_data=sql_injection_data,
        zip_path=None,
        created_at=datetime.now(timezone.utc),
        generated_at=None,
    )
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "src.adapters.api.intakes.CreateIntake.execute",
            AsyncMock(return_value=fake_project),
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/intakes",
                json={"intake_data": sql_injection_data},
            )

    assert response.status_code == 201
    assert response.json()["data"]["status"] == "intake_saved"


# ── S-002: Large payload (10MB+) rejected ──


@pytest.mark.anyio
async def test_large_payload_rejected(app):
    """S-002: Payloads over 10MB must be rejected."""
    large_data = "x" * (10 * 1024 * 1024 + 1)  # 10MB + 1 byte
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/intakes",
            content=f'{{"intake_data": {{"data": "{large_data}"}}}}',
            headers={"content-type": "application/json"},
        )

    assert response.status_code in (413, 400, 422)


# ── S-003: Malformed JSON handled gracefully ──


@pytest.mark.anyio
async def test_malformed_json_returns_error(app):
    """S-003: Malformed JSON body returns 400, no server crash."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/intakes",
            content="{invalid json!!!",
            headers={"content-type": "application/json"},
        )

    assert response.status_code in (400, 422)
    body = response.json()
    assert "error" in body
    assert "message" in body


@pytest.mark.anyio
async def test_malformed_json_generate_returns_error(app):
    """S-003: Malformed JSON on /generate returns 400."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/generate",
            content="{not valid json",
            headers={"content-type": "application/json"},
        )

    assert response.status_code in (400, 422)
    body = response.json()
    assert "error" in body


# ── S-004: Path traversal in project_id rejected ──


@pytest.mark.anyio
async def test_path_traversal_in_project_id_rejected(app):
    """S-004: Path traversal strings in project_id are rejected (404 from routing or 422 from validation)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # URL-based path traversal is blocked by routing (404) - safe
        response = await client.get("/projects/../../etc/passwd")
        assert response.status_code in (404, 422)

        # Non-UUID path-like strings reaching the handler get 422
        response = await client.get("/projects/etc-passwd-traversal")
        assert response.status_code == 422
        assert response.json()["error"] == "INVALID_PROJECT_ID"


@pytest.mark.anyio
async def test_path_traversal_in_download_rejected(app):
    """S-004: Path traversal in download endpoint is rejected."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/projects/../../etc/passwd/download")
        assert response.status_code in (404, 422)

        response = await client.get("/projects/etc-passwd-traversal/download")
        assert response.status_code == 422
        assert response.json()["error"] == "INVALID_PROJECT_ID"


@pytest.mark.anyio
async def test_path_traversal_in_generate_rejected(app):
    """S-004: Path traversal in generate body returns 422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/generate",
            json={"project_id": "../../etc/passwd"},
        )

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "INVALID_PROJECT_ID"


# ── S-005: Empty body handled gracefully ──


@pytest.mark.anyio
async def test_empty_body_intakes_returns_error(app):
    """S-005: Empty body on POST /intakes returns 400."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/intakes",
            content="",
            headers={"content-type": "application/json"},
        )

    assert response.status_code in (400, 422)
    body = response.json()
    assert "error" in body


@pytest.mark.anyio
async def test_empty_body_generate_returns_error(app):
    """S-005: Empty body on POST /generate returns 400."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/generate",
            content="",
            headers={"content-type": "application/json"},
        )

    assert response.status_code in (400, 422)
    body = response.json()
    assert "error" in body
