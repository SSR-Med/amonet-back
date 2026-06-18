from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class OrdenProduccionVariableGlobal:
    id: UUID = field(default_factory=uuid4)
    amonet_orden_produccion_id: UUID = field(default_factory=uuid4)
    amonet_variable_materia_prima_id: UUID = field(default_factory=uuid4)
    cantidad: int = 0
