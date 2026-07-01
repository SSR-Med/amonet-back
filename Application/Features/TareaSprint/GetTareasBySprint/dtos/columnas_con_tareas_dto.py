from typing import List
from uuid import UUID


class ColumnaInfoDto:
    def __init__(self, id: UUID, nombre: str, posicion: int) -> None:
        self.id = id
        self.nombre = nombre
        self.posicion = posicion


class ColumnaConTareasDto:
    def __init__(
        self,
        columna: ColumnaInfoDto,
        tareas: List,
    ) -> None:
        self.columna = columna
        self.tareas = tareas
