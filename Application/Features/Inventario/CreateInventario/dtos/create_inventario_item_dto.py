from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator


class ContenedorInputDto(BaseModel):
    cantidad: int
    precio: int


class CreateInventarioItemDto(BaseModel):
    amonet_materia_prima_id: UUID
    proveedor: str
    lote: str
    fecha_vencimiento: datetime
    contenedores: List[ContenedorInputDto]

    @field_validator("contenedores")
    @classmethod
    def validate_contenedores(cls, v: List[ContenedorInputDto]) -> List[ContenedorInputDto]:
        if not v:
            raise ValueError("At least one contenedor is required")
        for c in v:
            if c.cantidad < 0:
                raise ValueError("Cantidad must be >= 0")
            if c.precio < 0:
                raise ValueError("Precio must be >= 0")
        return v
