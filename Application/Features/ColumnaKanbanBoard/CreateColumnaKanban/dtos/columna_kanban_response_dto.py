from datetime import datetime
from typing import Optional
from uuid import UUID


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class ColumnaKanbanResponseDto:
    def __init__(
        self,
        id: UUID,
        nombre: str,
        posicion: int,
        usuario_alta: UsuarioInfoDto,
        fecha_alta: datetime,
        usuario_modifica: Optional[UsuarioInfoDto] = None,
        fecha_modifica: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.nombre = nombre
        self.posicion = posicion
        self.usuario_alta = usuario_alta
        self.fecha_alta = fecha_alta
        self.usuario_modifica = usuario_modifica
        self.fecha_modifica = fecha_modifica
