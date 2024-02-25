from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, Update, update
from repositories.base import (
    MixinDeleteRepository,
    MixinCreateRepository,
    MixinUpdateRepository,
)


class SQLAlchemyRepository(
    MixinCreateRepository, MixinDeleteRepository, MixinUpdateRepository
):
    _model = None
    _statement: Select | Update | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def reset_statement(self):
        self._statement = None

    @staticmethod
    def to_pydantic(db_obj, pydantic_model):
        return pydantic_model(**db_obj.__dict__)

    async def read(self):
        try:
            result = await self.session.execute(self._statement)
        finally:
            await self.session.close()
            self.reset_statement()
        return result.scalars().all()

    async def read_one(self):
        try:
            result = await self.session.execute(self._statement)
        finally:
            await self.session.close()
            self.reset_statement()
        return result.scalars().one()

    async def delete(self):
        return  # TODO(MosyaginGrigorii)

    async def update(self, orm_field, where_cond, update_data):
        self._statement = (
            update(self._model).where(where_cond == orm_field).values(**update_data)
        )
        await self.session.execute(self._statement)
        await self.session.commit()

    async def create(self, entity_model):
        db_obj = self._model(**entity_model.dict())
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.commit()
        return db_obj
