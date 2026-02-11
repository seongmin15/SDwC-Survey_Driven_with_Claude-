import os

import pytest


@pytest.fixture
def app():
    from src.config.app import create_app
    return create_app()


@pytest.fixture
def app_with_db():
    """Real DB connection (requires running PostgreSQL)."""
    os.environ.setdefault(
        "POSTGRESQL_URL",
        "postgresql+psycopg://sdwc:sdwc@localhost:5432/sdwc",
    )
    from src.config.app import create_app
    return create_app()


@pytest.fixture
def app_with_bad_db():
    """Intentionally broken DB URL to test failure handling."""
    os.environ["POSTGRESQL_URL"] = (
        "postgresql+psycopg://bad:bad@localhost:59999/nonexistent"
    )
    from src.config.app import create_app
    app = create_app()
    # Reset env after fixture creation
    os.environ.pop("POSTGRESQL_URL", None)
    return app
