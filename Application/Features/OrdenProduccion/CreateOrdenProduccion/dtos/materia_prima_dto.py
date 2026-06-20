from typing import List
from uuid import UUID

from pydantic import BaseModel

from .materia_prima_contenedor_dto import MateriaPrimaContenedorDto


class MateriaPrimaDto(BaseModel):
    amonet_materia_prima_id: UUID
    cantidad: int
    contenedores: List[MateriaPrimaContenedorDto]
