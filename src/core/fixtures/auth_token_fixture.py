import pytest

from src.core.config import Config


@pytest.fixture(scope="session")
def auth_token() -> str:
    return Config.api_key()