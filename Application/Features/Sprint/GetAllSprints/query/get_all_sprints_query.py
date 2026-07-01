from datetime import datetime
from typing import Optional

from core.dtos import PaginationQuery


class GetAllSprintsQuery(PaginationQuery):
    fecha_inicial: Optional[datetime] = None
    fecha_final: Optional[datetime] = None
    principal: Optional[bool] = None
    contador: Optional[int] = None
