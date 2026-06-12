from uuid import uuid4

from Application.Features.Usuario.CreateUsuario.command import (
    CreateUsuarioCommand,
)
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.services import PasswordService


class CreateUsuarioMapper:

    @staticmethod
    def to_model(dto: CreateUsuarioCommand) -> UsuarioConfiguration:
        return UsuarioConfiguration(
            id_amonet_usuario=uuid4(),
            documento=dto.documento,
            nombre=dto.nombre,
            rol=dto.rol.strip().upper(),
            password=PasswordService.hash(dto.password),
            activo=True,
        )
