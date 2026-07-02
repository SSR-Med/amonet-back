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
        if dto.titulo is not None:
            model.titulo = dto.titulo
        if dto.descripcion is not None:
            model.descripcion = dto.descripcion
        if dto.asignado is not None:
            model.asignado = dto.asignado
        if dto.fecha_vencimiento is not None:
            model.fecha_vencimiento = dto.fecha_vencimiento
        if dto.amonet_prioridad_kanban_id is not None:
            model.amonet_prioridad_kanban_id = dto.amonet_prioridad_kanban_id
        if dto.tags is not None:
            model.tags = [str(t) for t in dto.tags]
        if dto.amonet_sprint_id is not None:
            model.amonet_sprint_id = dto.amonet_sprint_id
        if dto.amonet_columna_kanban_id is not None:
            model.amonet_columna_kanban_id = dto.amonet_columna_kanban_id
        model.usuario_modifica = usuario_modifica
        model.fecha_modifica = datetime.now(timezone.utc)
        return model
