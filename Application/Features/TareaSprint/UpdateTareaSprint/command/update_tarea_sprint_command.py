from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class UpdateTareaSprintCommand(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    asignado: Optional[UUID] = None
    fecha_vencimiento: Optional[datetime] = None
    amonet_prioridad_kanban_id: Optional[UUID] = None
    tags: Optional[List[UUID]] = None
    amonet_sprint_id: Optional[UUID] = None
    amonet_columna_kanban_id: Optional[UUID] = None
