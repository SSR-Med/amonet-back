from datetime import datetime
from typing import Optional
from uuid import UUID


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class SprintResponseDto:
    def __init__(
        self,
        id: UUID,
        contador: int,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime],
        activo: bool,
        principal: bool,
        descripcion: Optional[str],
        usuario_alta: UsuarioInfoDto,
        usuario_modifica: Optional[UsuarioInfoDto] = None,
        fecha_modifica: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.contador = contador
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activo = activo
        self.principal = principal
        self.descripcion = descripcion
        self.usuario_alta = usuario_alta
        self.usuario_modifica = usuario_modifica
        self.fecha_modifica = fecha_modifica
