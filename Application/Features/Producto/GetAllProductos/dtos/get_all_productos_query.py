from typing import Optional
from uuid import UUID

from core.dtos import PaginationQuery


class GetAllProductosQuery(PaginationQuery):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    id_amonet_marca: Optional[UUID] = None
