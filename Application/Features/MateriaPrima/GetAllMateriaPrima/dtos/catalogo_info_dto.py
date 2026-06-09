from typing import Optional
from uuid import UUID


class CatalogoInfoDto:
    def __init__(self, id: UUID, nombre: str, abreviacion: Optional[str] = None) -> None:
        self.id = id
        self.nombre = nombre
        self.abreviacion = abreviacion
