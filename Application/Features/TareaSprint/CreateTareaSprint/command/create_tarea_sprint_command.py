from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class CreateTareaSprintCommand(BaseModel):
    titulo: str
    descripcion: str
    asignado: UUID
    fecha_vencimiento: Optional[datetime] = None
    amonet_prioridad_kanban_id: Optional[UUID] = None
    tags: Optional[List[UUID]] = None
    amonet_sprint_id: UUID
    amonet_columna_kanban_id: UUID
