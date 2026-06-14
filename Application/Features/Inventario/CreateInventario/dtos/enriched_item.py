from datetime import datetime
from typing import Optional
from uuid import UUID

from Application.Features.Inventario.CreateInventario.dtos import (
    CreateInventarioItemDto,
)


class EnrichedItem:
    def __init__(
        self,
        dto: CreateInventarioItemDto,
        fecha_ingreso: datetime,
        numero_ingreso: str,
        usuario_alta: UUID,
    ) -> None:
        self.dto = dto
        self.fecha_ingreso = fecha_ingreso
        self.numero_ingreso = numero_ingreso
        self.usuario_alta = usuario_alta
        self.status: Optional[bool] = None
