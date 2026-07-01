from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class ComentarioTarea:
    id: UUID = field(default_factory=uuid4)
    amonet_tarea_sprint_id: UUID = field(default_factory=uuid4)
    comentario: str = ""
    activo: bool = True
    usuario_alta: UUID = field(default_factory=uuid4)
    fecha_alta: Optional[datetime] = None
    fecha_modifica: Optional[datetime] = None
