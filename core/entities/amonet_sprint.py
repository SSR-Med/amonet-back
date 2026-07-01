from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Sprint:
    id: UUID = field(default_factory=uuid4)
    contador: int = 0
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    activo: bool = True
    principal: bool = False
    descripcion: Optional[str] = None
    usuario_alta: UUID = field(default_factory=uuid4)
    usuario_modifica: Optional[UUID] = None
    fecha_modifica: Optional[datetime] = None
