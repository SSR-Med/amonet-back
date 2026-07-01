from typing import Optional

from core.dtos import PaginationQuery


class GetAllColumnaKanbanQuery(PaginationQuery):
    nombre: Optional[str] = None
    posicion: Optional[int] = None
