from typing import Any, Callable, Generic, List, Optional, Tuple, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.interfaces import IRepository

T = TypeVar("T")


class Repository(IRepository, Generic[T]):

    def __init__(self, session: AsyncSession, model_class: Type[T]) -> None:
        self._session = session
        self._model = model_class

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        where: Optional[Callable] = None,
        loader_options: Optional[List[Any]] = None,
        order_by: Optional[Any] = None,
    ) -> Tuple[List[T], int, int, int]:
        query = select(self._model)
        count_query = select(func.count()).select_from(self._model)

        if where:
            query = where(query)
            count_query = where(count_query)

        if loader_options:
            query = query.options(*loader_options)

        if order_by is not None:
            query = query.order_by(order_by)

        total_result = await self._session.execute(count_query)
        total_items = total_result.scalar_one()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self._session.execute(query)
        items = list(result.scalars().all())

        return items, page, total_items, page_size

    async def first_or_default(
        self, where: Callable, loader_options: Optional[List[Any]] = None
    ) -> Optional[T]:
        query = select(self._model)
        if where:
            query = where(query)
        if loader_options:
            query = query.options(*loader_options)
        query = query.limit(1)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, where: Callable) -> None:
        from sqlalchemy import delete as sa_delete

        query = sa_delete(self._model)
        if where:
            query = where(query)
        await self._session.execute(query)

    async def create(self, entity: T) -> None:
        self._session.add(entity)

    async def update(self, entity: T) -> None:
        self._session.merge(entity)
