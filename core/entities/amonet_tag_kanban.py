from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class TagKanban:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
    color_red: int = 0
    color_green: int = 0
    color_blue: int = 0
    activo: bool = True
