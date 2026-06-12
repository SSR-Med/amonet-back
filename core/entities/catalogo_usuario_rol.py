from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class CatalogoUsuarioRol:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
