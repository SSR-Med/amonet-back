from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class MateriaPrima:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
    id_cat_amonet_tipo_materia_prima: UUID = field(default_factory=uuid4)
    id_cat_amonet_tipo_unidad: UUID = field(default_factory=uuid4)
