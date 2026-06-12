from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.DeleteUsuario.command import (
    DeleteUsuarioCommand,
)
from core.dtos import CurrentUserDto
from core.exceptions import NotFoundException, UnauthorizedException
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class DeleteUsuarioCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, UsuarioConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(self, command: DeleteUsuarioCommand, current_user: CurrentUserDto) -> None:
        if command.id == current_user.id:
            raise UnauthorizedException("Cannot deactivate yourself")

        model = await self._repository.first_or_default(
            lambda q: q.where(UsuarioConfiguration.id_amonet_usuario == command.id)
        )
        if model is None:
            raise NotFoundException("Usuario", str(command.id))

        model.activo = False
        await self._repository.update(model)
        await self._unit_of_work.commit()
