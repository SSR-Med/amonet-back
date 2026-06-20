from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Producto:
    id: UUID = field(default_factory=uuid4)
    codigo: str = ""
    nombre: str = ""
    id_amonet_marca: UUID = field(default_factory=uuid4)
    status: bool = True
