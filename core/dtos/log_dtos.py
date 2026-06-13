from dataclasses import dataclass
from typing import Optional


@dataclass
class LogItemDto:
    nombre: str
    peso: Optional[int]
    fecha: str
    origen: str
