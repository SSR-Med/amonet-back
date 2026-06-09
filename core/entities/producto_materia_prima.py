from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class ProductoMateriaPrima:
    id: UUID = field(default_factory=uuid4)
    id_amonet_producto: UUID = field(default_factory=uuid4)
    id_amonet_materia_prima: UUID = field(default_factory=uuid4)
    formula: str = ""
