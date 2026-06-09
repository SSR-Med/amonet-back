from uuid import UUID

from pydantic import BaseModel


class MateriaPrimaEnProductoDto(BaseModel):
    id_amonet_materia_prima: UUID
    formula: str = ""
