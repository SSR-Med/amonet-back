from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class OrdenProduccion:
    id: UUID = field(default_factory=uuid4)
    observacion_creacion: str = ""
    descripcion: str = ""
    amonet_producto_id: UUID = field(default_factory=uuid4)
    fecha_alta: Optional[datetime] = None
    usuario_alta: UUID = field(default_factory=uuid4)
    fecha_modifica: Optional[datetime] = None
    usuario_modifica: Optional[UUID] = None
    amonet_estado_produccion_id: UUID = field(default_factory=uuid4)
    coste: float = 0.0
