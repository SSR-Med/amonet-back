from typing import Optional

from core.dtos import PaginationQuery


class GetAllUsuariosQuery(PaginationQuery):
    documento: Optional[str] = None
    rol: Optional[str] = None
