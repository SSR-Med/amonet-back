from typing import List

from Application.Features.Usuario.GetAllRoles.dtos import RolResponseDto
from infrastructure.dataaccess.configurations import (
    CatalogoUsuarioRolConfiguration,
)


class RolMapper:

    @staticmethod
    def to_response(model: CatalogoUsuarioRolConfiguration) -> RolResponseDto:
        return RolResponseDto(
            id=model.id_cat_amonet_usuario_rol,
            nombre=model.nombre,
        )

    @staticmethod
    def to_list_response(
        items: List[CatalogoUsuarioRolConfiguration],
    ) -> List[RolResponseDto]:
        return [RolMapper.to_response(item) for item in items]
