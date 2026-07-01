from datetime import datetime, timezone
from uuid import UUID, uuid4

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.command import (
    CreateColumnaKanbanCommand,
)
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration


class CreateColumnaKanbanMapper:

    @staticmethod
    def to_model(
        dto: CreateColumnaKanbanCommand, usuario_alta: UUID
    ) -> ColumnaKanbanConfiguration:
        return ColumnaKanbanConfiguration(
            id_amonet_columna_kanban=uuid4(),
            nombre=dto.nombre,
            posicion=dto.posicion,
            usuario_alta=usuario_alta,
            fecha_alta=datetime.now(timezone.utc),
        )
