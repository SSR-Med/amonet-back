from typing import Optional
from uuid import UUID

from core.dtos import PaginationQuery


class GetAllOrdenesProduccionQuery(PaginationQuery):
    fecha_min: Optional[str] = None
    fecha_max: Optional[str] = None
    amonet_producto_id: Optional[UUID] = None
    amonet_estado_produccion_id: Optional[UUID] = None
    amonet_materia_prima_id: Optional[UUID] = None
