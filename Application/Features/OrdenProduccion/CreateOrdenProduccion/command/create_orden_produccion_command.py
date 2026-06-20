from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from Application.Features.OrdenProduccion.CreateOrdenProduccion.dtos import (
    MateriaPrimaDto,
    VariableGlobalDto,
)


class CreateOrdenProduccionCommand(BaseModel):
    descripcion: str
    amonet_producto_id: UUID
    variables_globales: List[VariableGlobalDto] = []
    materias_primas: List[MateriaPrimaDto]
    observaciones: Optional[str] = None

    @field_validator("descripcion")
    @classmethod
    def trim_upper_descripcion(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("observaciones")
    @classmethod
    def trim_upper_observaciones(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return v.strip().upper()
