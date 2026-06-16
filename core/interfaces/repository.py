from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):

    @abstractmethod
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        where: Optional[Callable] = None,
        loader_options: Optional[List[Any]] = None,
        order_by: Optional[Any] = None,
    ) -> Tuple[List[T], int, int, int]:
        pass

    @abstractmethod
    async def first_or_default(
        self, where: Callable, loader_options: Optional[List[Any]] = None
    ) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, where: Callable) -> None:
        pass

    @abstractmethod
    async def create(self, entity: T) -> None:
        pass

    @abstractmethod
    async def update(self, entity: T) -> None:
        pass
