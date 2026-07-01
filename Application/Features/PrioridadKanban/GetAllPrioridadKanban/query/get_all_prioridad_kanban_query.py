from typing import Optional

from core.dtos import PaginationQuery


class GetAllPrioridadKanbanQuery(PaginationQuery):
    nombre: Optional[str] = None
