from datetime import datetime, timezone
from uuid import UUID

from Application.Features.ColumnaKanbanBoard.UpdateColumnaKanban.command import (
    UpdateColumnaKanbanCommand,
)
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration


class UpdateColumnaKanbanMapper:

    @staticmethod
    def apply(
        model: ColumnaKanbanConfiguration,
        dto: UpdateColumnaKanbanCommand,
        usuario_modifica: UUID,
    ) -> ColumnaKanbanConfiguration:
        model.nombre = dto.nombre
        model.posicion = dto.posicion
        model.usuario_modifica = usuario_modifica
        model.fecha_modifica = datetime.now(timezone.utc)
        return model
