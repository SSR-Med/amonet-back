from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class ColumnaKanban:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
    posicion: int = 0
    activo: bool = True
    usuario_alta: UUID = field(default_factory=uuid4)
    fecha_alta: Optional[datetime] = None
    usuario_modifica: Optional[UUID] = None
    fecha_modifica: Optional[datetime] = None
