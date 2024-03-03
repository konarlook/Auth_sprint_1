import pytest
from alembic.command import upgrade


@pytest.fixture(scope="session", autouse=True)
def pg_migrate(alembconfig_from_url):
    upgrade(alembconfig_from_url, "head")
