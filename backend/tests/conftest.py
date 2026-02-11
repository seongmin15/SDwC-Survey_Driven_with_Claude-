import pytest


@pytest.fixture
def app():
    from src.config.app import create_app
    return create_app()
