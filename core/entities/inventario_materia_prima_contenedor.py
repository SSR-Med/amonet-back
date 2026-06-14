from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class InventarioMateriaPrimaContenedor:
    id: UUID = field(default_factory=uuid4)
    contador_materia_prima: int = 0
    cantidad: float = 0.0
    amonet_inventario_materia_prima_id: UUID = field(default_factory=uuid4)
