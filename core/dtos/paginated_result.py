from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    items: List[T]
    current_page: int
    total_items: int
    page_size: int
