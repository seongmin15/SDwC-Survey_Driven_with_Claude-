import pytest


@pytest.fixture(params=["asyncio"])
def anyio_backend(request):
    """Integration tests use asyncio only (psycopg3 requirement)."""
    return request.param
