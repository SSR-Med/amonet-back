from typing import List

from pydantic import BaseModel

from Application.Features.Inventario.CreateInventario.dtos import (
    CreateInventarioItemDto,
)


class CreateInventarioCommand(BaseModel):
    items: List[CreateInventarioItemDto]
    archivo: bytes
    nombre_archivo: str
