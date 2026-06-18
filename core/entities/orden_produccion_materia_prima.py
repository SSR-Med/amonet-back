from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class OrdenProduccionMateriaPrima:
    id: UUID = field(default_factory=uuid4)
    amonet_materia_prima_id: UUID = field(default_factory=uuid4)
    amonet_orden_produccion_id: UUID = field(default_factory=uuid4)
