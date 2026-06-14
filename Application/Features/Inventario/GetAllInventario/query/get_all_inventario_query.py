from typing import Optional
from uuid import UUID

from core.dtos import PaginationQuery


class GetAllInventarioQuery(PaginationQuery):
    status: Optional[bool] = None
    lote: Optional[str] = None
    amonet_materia_prima_id: Optional[UUID] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    proveedor: Optional[str] = None
    usuario_alta: Optional[UUID] = None
