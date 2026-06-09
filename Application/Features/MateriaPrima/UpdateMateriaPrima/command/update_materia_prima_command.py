from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UpdateMateriaPrimaCommand(BaseModel):
    id: Optional[UUID] = None
    nombre: str
    id_cat_amonet_tipo_materia_prima: UUID
    id_cat_amonet_tipo_unidad: UUID
