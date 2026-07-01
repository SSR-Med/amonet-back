from datetime import datetime
from uuid import UUID, uuid4

from Application.Features.Sprint.CreateSprint.command import (
    CreateSprintCommand,
)
from infrastructure.dataaccess.configurations import SprintConfiguration


class CreateSprintMapper:

    @staticmethod
    def to_model(
        dto: CreateSprintCommand,
        usuario_alta: UUID,
        fecha_inicio: datetime,
    ) -> SprintConfiguration:
        return SprintConfiguration(
            id_amonet_sprint=uuid4(),
            fecha_inicio=fecha_inicio,
            principal=True,
            descripcion=dto.descripcion,
            usuario_alta=usuario_alta,
        )
