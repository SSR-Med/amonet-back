from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class TareaSprint:
    id: UUID = field(default_factory=uuid4)
    titulo: str = ""
    descripcion: str = ""
    activo: bool = True
    asignado: UUID = field(default_factory=uuid4)
    amonet_sprint_id: UUID = field(default_factory=uuid4)
    amonet_columna_kanban_id: UUID = field(default_factory=uuid4)
    fecha_vencimiento: Optional[datetime] = None
    tags: Optional[list] = None
    amonet_prioridad_kanban_id: Optional[UUID] = None
    usuario_alta: UUID = field(default_factory=uuid4)
    fecha_alta: Optional[datetime] = None
    usuario_modifica: Optional[UUID] = None
    fecha_modifica: Optional[datetime] = None
