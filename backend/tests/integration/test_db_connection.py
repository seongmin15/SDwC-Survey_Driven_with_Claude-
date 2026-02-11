"""
Integration tests for database connection.
Verification IDs: I-001, I-002
"""
import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.anyio
async def test_db_connection_success_ready_200(app_with_db):
    """I-001: 앱 시작 시 PostgreSQL 연결 성공 → /ready 200"""
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.anyio
async def test_db_connection_failure_ready_503(app_with_bad_db):
    """I-002: DB 연결 실패 시 /ready → 503"""
    transport = ASGITransport(app=app_with_bad_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/ready")
    assert response.status_code == 503
