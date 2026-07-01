from datetime import datetime, timezone
from uuid import UUID

from Application.Features.Sprint.UpdateSprint.command import (
    UpdateSprintCommand,
)
from infrastructure.dataaccess.configurations import SprintConfiguration


class UpdateSprintMapper:

    @staticmethod
    def apply(
        model: SprintConfiguration,
        dto: UpdateSprintCommand,
        usuario_modifica: UUID,
    ) -> SprintConfiguration:
        if dto.principal is not None:
            model.principal = dto.principal
        if dto.descripcion is not None:
            model.descripcion = dto.descripcion
        model.usuario_modifica = usuario_modifica
        model.fecha_modifica = datetime.now(timezone.utc)
        return model
