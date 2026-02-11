"""
Contract tests for POST /intakes.
Verification IDs: C-001, C-002, C-003, C-004, C-005, C-006
"""
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, patch

VALID_INTAKE_DATA = {
    "project": {"name": "test-app", "description": "A test", "target_users": "devs", "core_value": "testing"},
    "scope": {"in_scope": ["feature A"], "out_of_scope": "none"},
    "architecture": {"pattern": "monolith", "internal_style": "hexagonal"},
    "services": ["backend_api"],
    "backend": {"language": "python", "framework": "fastapi"},
}


@pytest.fixture
def app():
    """Fresh app for each test (no DB mocking needed — use case is mocked)."""
    from src.config.app import create_app
    return create_app()


@pytest.mark.anyio
async def test_valid_intake_returns_201(app):
    """C-001: 유효한 intake_data → 201 Created, project_id 반환"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/intakes", json={"intake_data": VALID_INTAKE_DATA})
    assert response.status_code == 201
    body = response.json()
    assert "data" in body
    assert "project_id" in body["data"]
    assert body["data"]["status"] == "intake_saved"
    assert "created_at" in body["data"]


@pytest.mark.anyio
async def test_missing_intake_data_returns_400(app):
    """C-002: intake_data 필드 누락 → 400"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/intakes", json={"other_field": "value"})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "MISSING_REQUIRED_FIELD"


@pytest.mark.anyio
async def test_schema_validation_failure_returns_400(app):
    """C-003: 필수 하위 필드 누락 → 400"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/intakes", json={"intake_data": {"missing": "project_name"}})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "INVALID_INTAKE_DATA"


@pytest.mark.anyio
async def test_wrong_type_returns_400(app):
    """C-004: intake_data가 잘못된 타입 → 400"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/intakes", json={"intake_data": "not_an_object"})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "INVALID_INTAKE_DATA"


@pytest.mark.anyio
async def test_empty_body_returns_400(app):
    """C-005: 빈 JSON body → 400"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/intakes", json={})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "MISSING_REQUIRED_FIELD"


@pytest.mark.anyio
async def test_wrong_content_type_returns_error(app):
    """C-006: Content-Type이 application/json이 아님 → 에러"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/intakes",
            content="intake_data=test",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    assert response.status_code in (415, 422)
