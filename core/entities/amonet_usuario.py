from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Usuario:
    id: UUID = field(default_factory=uuid4)
    documento: str = ""
    nombre: str = ""
    rol: str = "OPERARIO"
    password: str = ""
