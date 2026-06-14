from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class CreateInventarioItemDto(BaseModel):
    amonet_materia_prima_id: UUID
    proveedor: str
    lote: str
    fecha_vencimiento: datetime
    cantidades: List[int]
