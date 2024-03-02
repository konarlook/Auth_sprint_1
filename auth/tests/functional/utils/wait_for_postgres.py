from subsidiary.backoff import backoff
from sqlalchemy_utils import database_exists
from tests.functional.core.settings import test_settings


@backoff(connect_exception=ConnectionError)
def pinging_elastic(pg_url: str):
    """Waiting for test Elasticsearch service response"""
    return database_exists(pg_url)


if __name__ == "__main__":
    pg_url = str(test_settings.database_url_psycopg)
    pinging_elastic(pg_url=pg_url)
