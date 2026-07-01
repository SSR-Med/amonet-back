from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class TareaSprint:
    id: UUID = field(default_factory=uuid4)
    titulo: str = ""
    descripcion: str = ""
    posicion: int = 0
    amonet_sprint_id: UUID = field(default_factory=uuid4)
    amonet_columna_kanban_id: UUID = field(default_factory=uuid4)
    usuario_alta: UUID = field(default_factory=uuid4)
    fecha_alta: Optional[datetime] = None
    usuario_modifica: Optional[UUID] = None
    fecha_modifica: Optional[datetime] = None
