from uuid import UUID

from core.constants import ADMIN
from core.dtos import CurrentUserDto
from core.exceptions import UnauthorizedException
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration


class UpdateComentarioTareaValidator:

    def validate(self, model: ComentarioTareaConfiguration, current_user: CurrentUserDto) -> None:
        if model.usuario_alta != current_user.id and current_user.rol != ADMIN:
            raise UnauthorizedException("You can only edit your own comments")
