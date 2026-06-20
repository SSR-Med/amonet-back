from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class OrdenProduccionMateriaPrimaContenedor:
    id: UUID = field(default_factory=uuid4)
    amonet_inventario_materia_prima_contenedor_id: UUID = field(default_factory=uuid4)
    amonet_orden_produccion_materia_prima_id: UUID = field(default_factory=uuid4)
    cantidad: int = 0
    coste: float = 0.0
