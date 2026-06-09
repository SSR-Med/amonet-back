from typing import Optional

from core.dtos import PaginationQuery


class GetAllMarcasQueryDto(PaginationQuery):
    nombre: Optional[str] = None
