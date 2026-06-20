from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class VariablesGlobalesMateriaPrima:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
    status: bool = True
