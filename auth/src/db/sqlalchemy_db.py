from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import settings

engine = create_async_engine(
    url=settings.postgres.database_url_asyncpg,
    echo=settings.debug_mode,
    future=True,
)

session = AsyncSession(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
