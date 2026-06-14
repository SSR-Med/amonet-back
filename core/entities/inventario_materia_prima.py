from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class InventarioMateriaPrima:
    id: UUID = field(default_factory=uuid4)
    fecha_ingreso: Optional[datetime] = None
    numero_ingreso: str = ""
    amonet_materia_prima_id: UUID = field(default_factory=uuid4)
    proveedor: str = ""
    lote: str = ""
    fecha_vencimiento: Optional[datetime] = None
    usuario_alta: UUID = field(default_factory=uuid4)
    status: Optional[bool] = None
    usuario_modifica: Optional[UUID] = None
    ruta_evidencia: str = ""
