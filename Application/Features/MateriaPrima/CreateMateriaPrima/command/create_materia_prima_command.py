from uuid import UUID

from pydantic import BaseModel


class CreateMateriaPrimaCommand(BaseModel):
    nombre: str
    id_cat_amonet_tipo_materia_prima: UUID
    id_cat_amonet_tipo_unidad: UUID
