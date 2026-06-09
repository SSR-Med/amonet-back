from uuid import UUID

from pydantic import BaseModel

from Application.Features.Producto.CreateProducto.dtos.materia_prima_en_producto_dto import (
    MateriaPrimaEnProductoDto,
)


class CreateProductoCommand(BaseModel):
    codigo: str
    nombre: str
    id_amonet_marca: UUID
    materias_primas: list[MateriaPrimaEnProductoDto] = []
