import asyncio
import json

import aiohttp
import pytest_asyncio
from alembic.command import upgrade
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tests.functional.core.settings import test_settings


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
def pg_migrate(alembconfig_from_url):
    upgrade(alembconfig_from_url, "head")


@pytest_asyncio.fixture(name="aiohttp_session", scope="session")
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name="sqlalchemy_session", scope="session")
async def sqlalchemy_session():
    engine = create_async_engine(test_settings.database_url_asyncpg)
    async_factory = async_sessionmaker(engine)
    async with async_factory() as session:
        yield session


@pytest_asyncio.fixture(name="redis_client", scope="session")
async def redis_client():
    redis_client = Redis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
        db=test_settings.redis_database,
    )
    yield redis_client
    await redis_client.close()


@pytest_asyncio.fixture(name="redis_read_data")
def redis_read_data(redis_client):
    async def inner(key: str):
        data = await redis_client.get(str(key))
        if not data:
            return None

        return json.loads(data)

    return inner


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(aiohttp_session):
    async def inner(url: str, query_data: dict):
        async with aiohttp_session.get(
            url, params=query_data, raise_for_status=True
        ) as response:
            return await response.json(), response.status

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(aiohttp_session):
    async def inner(url: str, query_data: dict):
        async with aiohttp_session.post(
            url, params=query_data, raise_for_status=True
        ) as response:
            return await response.json(), response.status

    return inner


# @pytest_asyncio.fixture(name="create_user", scope="session")
# def create_user(sqlalchemy_session):
#     async def inner(user_data):
#         user_repo = user_data_repository.get_database_client(sqlalchemy_session)
#         user = CreateUserSchema(
#             email="me@gpn.ru",
#             user_name="user_name",
#             first_name="first_name",
#             last_name="last_name",
#             phone_number="123",
#             hashed_password="123",
#         )
#         db_obj = await user_repo.create_user(user)
#         return db_obj
#
#     return inner


@pytest_asyncio.fixture(name="execute_raw_sql", scope="session")
def execute_raw_sql(sqlalchemy_session):
    async def inner(sql: str):
        sql_text = text(sql)
        await sqlalchemy_session.execute(sql_text)
        await sqlalchemy_session.commit()

    return inner
