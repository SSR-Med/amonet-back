from sqlalchemy.ext.asyncio import AsyncSession

from core.interfaces import IUnitOfWork


class UnitOfWork(IUnitOfWork):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args) -> None:
        exc_type, exc_val, exc_tb = args
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self._session.close()
