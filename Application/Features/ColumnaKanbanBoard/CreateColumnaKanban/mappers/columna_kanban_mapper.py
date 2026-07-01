from typing import Optional

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
    UsuarioInfoDto,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration


class ColumnaKanbanMapper:

    @staticmethod
    def to_response(
        model: ColumnaKanbanConfiguration,
        current_user: Optional[CurrentUserDto] = None,
    ) -> ColumnaKanbanResponseDto:
        usuario_alta_rel = model.usuario_alta_rel
        usuario_modifica_rel = model.usuario_modifica_rel

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

        if usuario_modifica_rel is not None:
            usuario_modifica = UsuarioInfoDto(
                id=usuario_modifica_rel.id_amonet_usuario,
                documento=usuario_modifica_rel.documento,
                nombre=usuario_modifica_rel.nombre,
            )
        else:
            usuario_modifica = None

        return ColumnaKanbanResponseDto(
            id=model.id_amonet_columna_kanban,
            nombre=model.nombre,
            posicion=model.posicion,
            usuario_alta=usuario_alta,
            fecha_alta=model.fecha_alta,
            usuario_modifica=usuario_modifica,
            fecha_modifica=model.fecha_modifica,
        )


class ColumnaKanbanLoaderOptions:

    @staticmethod
    def get():
        from sqlalchemy.orm import selectinload

        return [
            selectinload(ColumnaKanbanConfiguration.usuario_alta_rel),
            selectinload(ColumnaKanbanConfiguration.usuario_modifica_rel),
        ]
