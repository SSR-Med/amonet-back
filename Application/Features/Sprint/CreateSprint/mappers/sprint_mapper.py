from typing import Optional

from sqlalchemy.orm import selectinload

from Application.Features.Sprint.CreateSprint.dtos import (
    SprintResponseDto,
    UsuarioInfoDto,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess.configurations import SprintConfiguration


class SprintMapper:

    @staticmethod
    def to_response(
        model: SprintConfiguration,
        current_user: Optional[CurrentUserDto] = None,
    ) -> SprintResponseDto:
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

        usuario_modifica_rel = model.usuario_modifica_rel
        if usuario_modifica_rel is not None:
            usuario_modifica = UsuarioInfoDto(
                id=usuario_modifica_rel.id_amonet_usuario,
                documento=usuario_modifica_rel.documento,
                nombre=usuario_modifica_rel.nombre,
            )
        else:
            usuario_modifica = None

        return SprintResponseDto(
            id=model.id_amonet_sprint,
            contador=model.contador,
            fecha_inicio=model.fecha_inicio,
            fecha_fin=model.fecha_fin,
            activo=model.activo,
            principal=model.principal,
            descripcion=model.descripcion,
            usuario_alta=usuario_alta,
            usuario_modifica=usuario_modifica,
            fecha_modifica=model.fecha_modifica,
        )


class SprintLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(SprintConfiguration.usuario_alta_rel),
            selectinload(SprintConfiguration.usuario_modifica_rel),
        ]
