from typing import Optional

from sqlalchemy.orm import selectinload

from Application.Features.ComentarioTarea.CreateComentarioTarea.dtos import (
    ComentarioTareaResponseDto,
    UsuarioInfoDto,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration


class ComentarioTareaMapper:

    @staticmethod
    def to_response(
        model: ComentarioTareaConfiguration,
        current_user: Optional[CurrentUserDto] = None,
    ) -> ComentarioTareaResponseDto:
        usuario_alta_rel = model.usuario_alta_rel

        if usuario_alta_rel is not None:
            usuario_alta = UsuarioInfoDto(
                id=usuario_alta_rel.id_amonet_usuario,
                documento=usuario_alta_rel.documento,
                nombre=usuario_alta_rel.nombre,
            )
        elif current_user is not None:
            usuario_alta = UsuarioInfoDto(
                id=current_user.id,
                documento=current_user.documento,
                nombre=current_user.nombre,
            )
        else:
            usuario_alta = UsuarioInfoDto(
                id=model.usuario_alta, documento="", nombre=""
            )

        return ComentarioTareaResponseDto(
            id=model.id_amonet_comentario_tarea,
            amonet_tarea_sprint_id=model.amonet_tarea_sprint_id,
            comentario=model.comentario,
            activo=model.activo,
            usuario_alta=usuario_alta,
            fecha_alta=model.fecha_alta,
            fecha_modifica=model.fecha_modifica,
        )


class ComentarioTareaLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(ComentarioTareaConfiguration.usuario_alta_rel),
        ]
