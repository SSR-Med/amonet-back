from typing import Optional
from uuid import UUID

from core.dtos import PaginationQuery


class GetAllMateriaPrimaQuery(PaginationQuery):
    nombre: Optional[str] = None
    id_cat_amonet_tipo_materia_prima: Optional[UUID] = None
    id_cat_amonet_tipo_unidad: Optional[UUID] = None
