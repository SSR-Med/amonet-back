from datetime import datetime
from typing import List, Optional
from uuid import UUID

from core.dtos import PaginationQuery


class GetAllTareasSprintQuery(PaginationQuery):
    titulo: Optional[str] = None
    amonet_sprint_id: Optional[UUID] = None
    amonet_prioridad_kanban_id: Optional[UUID] = None
    tags: Optional[List[UUID]] = None
    fecha_min: Optional[datetime] = None
    fecha_max: Optional[datetime] = None
    usuario_alta: Optional[UUID] = None
