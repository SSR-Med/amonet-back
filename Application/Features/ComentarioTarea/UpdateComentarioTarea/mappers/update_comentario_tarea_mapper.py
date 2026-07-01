from datetime import datetime, timezone

from Application.Features.ComentarioTarea.UpdateComentarioTarea.command import (
    UpdateComentarioTareaCommand,
)
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration


class UpdateComentarioTareaMapper:

    @staticmethod
    def apply(
        model: ComentarioTareaConfiguration,
        dto: UpdateComentarioTareaCommand,
    ) -> ComentarioTareaConfiguration:
        model.comentario = dto.comentario
        model.fecha_modifica = datetime.now(timezone.utc)
        return model
