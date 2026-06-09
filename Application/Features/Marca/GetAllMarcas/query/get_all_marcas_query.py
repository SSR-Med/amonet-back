from typing import Optional

from core.dtos import PaginationQuery


class GetAllMarcasQuery(PaginationQuery):
    nombre: Optional[str] = None
