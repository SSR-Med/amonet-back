from datetime import datetime
from typing import List, Optional
from uuid import UUID


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class TagInfoDto:
    def __init__(self, id: UUID, nombre: str, color_red: int, color_green: int, color_blue: int) -> None:
        self.id = id
        self.nombre = nombre
        self.color_red = color_red
        self.color_green = color_green
        self.color_blue = color_blue


class PrioridadInfoDto:
    def __init__(self, id: UUID, nombre: str, color_red: int, color_green: int, color_blue: int) -> None:
        self.id = id
        self.nombre = nombre
        self.color_red = color_red
        self.color_green = color_green
        self.color_blue = color_blue


class TareaSprintResponseDto:
    def __init__(
        self,
        id: UUID,
        titulo: str,
        descripcion: str,
        asignado: UsuarioInfoDto,
        amonet_sprint_id: UUID,
        amonet_columna_kanban_id: UUID,
        usuario_alta: UsuarioInfoDto,
        fecha_alta: datetime,
        fecha_vencimiento: Optional[datetime] = None,
        tags: Optional[List[TagInfoDto]] = None,
        prioridad: Optional['PrioridadInfoDto'] = None,
        usuario_modifica: Optional[UsuarioInfoDto] = None,
        fecha_modifica: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.asignado = asignado
        self.fecha_vencimiento = fecha_vencimiento
        self.tags = tags or []
        self.prioridad = prioridad
        self.amonet_sprint_id = amonet_sprint_id
        self.amonet_columna_kanban_id = amonet_columna_kanban_id
        self.usuario_alta = usuario_alta
        self.fecha_alta = fecha_alta
        self.usuario_modifica = usuario_modifica
        self.fecha_modifica = fecha_modifica
