from datetime import datetime, timezone
from uuid import UUID

from Application.Features.TareaSprint.UpdateTareaSprint.command import (
    UpdateTareaSprintCommand,
)
from infrastructure.dataaccess.configurations import TareaSprintConfiguration


class UpdateTareaSprintMapper:

    @staticmethod
    def apply(
        model: TareaSprintConfiguration,
        dto: UpdateTareaSprintCommand,
        usuario_modifica: UUID,
    ) -> TareaSprintConfiguration:
        model.titulo = dto.titulo
        model.descripcion = dto.descripcion
        model.asignado = dto.asignado
        model.fecha_vencimiento = dto.fecha_vencimiento
        model.amonet_prioridad_kanban_id = dto.amonet_prioridad_kanban_id
        model.tags = dto.tags
        model.amonet_sprint_id = dto.amonet_sprint_id
        model.amonet_columna_kanban_id = dto.amonet_columna_kanban_id
        model.usuario_modifica = usuario_modifica
        model.fecha_modifica = datetime.now(timezone.utc)
        return model
