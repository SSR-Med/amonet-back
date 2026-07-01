from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from Application.Features.TareaSprint.CreateTareaSprint.command import (
    CreateTareaSprintCommand,
)
from infrastructure.dataaccess.configurations import TareaSprintConfiguration


class CreateTareaSprintMapper:

    @staticmethod
    def to_model(
        dto: CreateTareaSprintCommand,
        usuario_alta: UUID,
    ) -> TareaSprintConfiguration:
        return TareaSprintConfiguration(
            id_amonet_tarea_sprint=uuid4(),
            titulo=dto.titulo,
            descripcion=dto.descripcion,
            asignado=dto.asignado,
            fecha_vencimiento=dto.fecha_vencimiento,
            amonet_prioridad_kanban_id=dto.amonet_prioridad_kanban_id,
            tags=dto.tags,
            amonet_sprint_id=dto.amonet_sprint_id,
            amonet_columna_kanban_id=dto.amonet_columna_kanban_id,
            usuario_alta=usuario_alta,
        )
