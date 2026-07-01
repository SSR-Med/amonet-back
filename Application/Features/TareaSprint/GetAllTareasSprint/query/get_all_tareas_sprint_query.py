from datetime import datetime
from typing import Optional
from uuid import UUID

from core.dtos import PaginationQuery


class GetAllTareasSprintQuery(PaginationQuery):
    amonet_sprint_id: Optional[UUID] = None
    fecha_min: Optional[datetime] = None
    fecha_max: Optional[datetime] = None
    usuario_alta: Optional[UUID] = None
