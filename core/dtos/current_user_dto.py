from dataclasses import dataclass
from uuid import UUID


@dataclass
class CurrentUserDto:
    id: UUID
    documento: str
    nombre: str
    rol: str
