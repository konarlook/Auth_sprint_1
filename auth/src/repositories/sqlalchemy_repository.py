from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base import (
    MixinDeleteRepository,
    MixinCreateRepository,
    MixinUpdateRepository,
)


class SQLAlchemyRepository(
    MixinCreateRepository, MixinDeleteRepository, MixinUpdateRepository
):
    _model = None
    _statement = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self):
        try:
            result = await self.session.execute(self._statement)
        finally:
            await self.session.close()
        return result.scalars().first()

    async def delete(self):
        return  # TODO(MosyaginGrigorii)

    async def update(self):
        return  # TODO(MosyaginGrigorii)

    async def create(self):
        return  # TODO(MosyaginGrigorii)
