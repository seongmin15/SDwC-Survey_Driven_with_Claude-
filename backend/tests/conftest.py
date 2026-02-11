import asyncio
import os
import sys
from unittest.mock import AsyncMock, patch

import pytest

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def app():
    """App fixture for contract tests (no real DB needed)."""
    with patch("src.adapters.api.health.check_connection", new_callable=AsyncMock, return_value=True):
        from src.config.app import create_app
        yield create_app()


@pytest.fixture
async def app_with_db():
    """Real DB connection (requires running PostgreSQL)."""
    os.environ.setdefault(
        "POSTGRESQL_URL",
        "postgresql+psycopg://sdwc:sdwc@localhost:5432/sdwc",
    )
    from src.config.database import init_engine, dispose_engine
    from src.config.settings import get_settings
    from src.config.app import create_app

    settings = get_settings()
    init_engine(settings.POSTGRESQL_URL)
    yield create_app()
    await dispose_engine()


@pytest.fixture
async def app_with_bad_db():
    """Intentionally broken DB URL to test failure handling."""
    from src.config.database import init_engine, dispose_engine
    from src.config.app import create_app

    init_engine("postgresql+psycopg://bad:bad@localhost:59999/nonexistent", connect_timeout=1)
    yield create_app()
    await dispose_engine()
