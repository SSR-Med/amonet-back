from uuid import UUID

from pydantic import BaseModel


class MateriaPrimaContenedorDto(BaseModel):
    amonet_inventario_materia_prima_contenedor_id: UUID
    cantidad: int
