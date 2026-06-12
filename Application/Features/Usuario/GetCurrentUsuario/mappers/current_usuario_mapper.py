from Application.Features.Usuario.GetCurrentUsuario.dtos import (
    CurrentUsuarioResponseDto,
)
from infrastructure.dataaccess.configurations import UsuarioConfiguration


class CurrentUsuarioMapper:

    @staticmethod
    def to_response(model: UsuarioConfiguration) -> CurrentUsuarioResponseDto:
        return CurrentUsuarioResponseDto(
            id=model.id_amonet_usuario,
            documento=model.documento,
            nombre=model.nombre,
            rol=model.rol,
        )
