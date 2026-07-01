from typing import Optional

from core.dtos import PaginationQuery


class GetAllTagsKanbanQuery(PaginationQuery):
    nombre: Optional[str] = None
