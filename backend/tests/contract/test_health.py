"""
Contract tests for GET /health and GET /ready endpoints.
Verification IDs: C-023, C-024
"""
import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.anyio
async def test_health_returns_200_ok(app):
    """C-023: GET /health -> 200 OK, {"status": "ok"}"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_ready_returns_200_ok(app):
    """C-024: GET /ready -> 200 OK, {"status": "ready"}"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
