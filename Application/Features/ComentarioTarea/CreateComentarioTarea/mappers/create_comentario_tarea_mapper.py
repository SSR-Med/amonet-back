from datetime import datetime, timezone
from uuid import UUID, uuid4

from Application.Features.ComentarioTarea.CreateComentarioTarea.command import (
    CreateComentarioTareaCommand,
)
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration


class CreateComentarioTareaMapper:

    @staticmethod
    def to_model(
        dto: CreateComentarioTareaCommand,
        usuario_alta: UUID,
    ) -> ComentarioTareaConfiguration:
        return ComentarioTareaConfiguration(
            id_amonet_comentario_tarea=uuid4(),
            amonet_tarea_sprint_id=dto.amonet_tarea_sprint_id,
            comentario=dto.comentario,
            usuario_alta=usuario_alta,
            fecha_alta=datetime.now(timezone.utc),
        )
