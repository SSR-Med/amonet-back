from datetime import datetime
from typing import Optional
from uuid import UUID


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class ComentarioTareaResponseDto:
    def __init__(
        self,
        id: UUID,
        amonet_tarea_sprint_id: UUID,
        comentario: str,
        activo: bool,
        usuario_alta: UsuarioInfoDto,
        fecha_alta: datetime,
        fecha_modifica: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.amonet_tarea_sprint_id = amonet_tarea_sprint_id
        self.comentario = comentario
        self.activo = activo
        self.usuario_alta = usuario_alta
        self.fecha_alta = fecha_alta
        self.fecha_modifica = fecha_modifica
