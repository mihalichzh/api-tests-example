import pytest
from faker.proxy import Faker


@pytest.fixture(scope="session")
def faker() -> Faker:
    return Faker()
