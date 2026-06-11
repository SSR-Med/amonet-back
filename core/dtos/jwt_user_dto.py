from dataclasses import dataclass
from uuid import UUID


@dataclass
class JwtUserDto:
    user_id: UUID
    documento: str
    nombre: str
    rol: str
