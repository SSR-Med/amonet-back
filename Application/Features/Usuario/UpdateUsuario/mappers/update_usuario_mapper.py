from typing import Optional

from Application.Features.Usuario.UpdateUsuario.command import (
    UpdateUsuarioCommand,
)
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.services import PasswordService


class UpdateUsuarioMapper:

    @staticmethod
    def apply(
        model: UsuarioConfiguration,
        dto: UpdateUsuarioCommand,
        new_password: Optional[str] = None,
    ) -> UsuarioConfiguration:
        if dto.documento is not None:
            model.documento = dto.documento
        if dto.nombre is not None:
            model.nombre = dto.nombre
        if dto.rol is not None:
            model.rol = dto.rol
        if new_password is not None:
            model.password = new_password
        return model
