from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator


class CreateInventarioItemDto(BaseModel):
    amonet_materia_prima_id: UUID
    proveedor: str
    lote: str
    fecha_vencimiento: datetime
    cantidades: List[int]

    @field_validator("cantidades")
    @classmethod
    def validate_cantidades(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("At least one cantidad is required")
        for c in v:
            if c < 0:
                raise ValueError("Cantidades must be >= 0")
        return v
