from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Marca.DeleteMarca.command import (
    DeleteMarcaCommand,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class DeleteMarcaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MarcaConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(self, command: DeleteMarcaCommand, current_user: CurrentUserDto) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == command.id)
        )
        if model is None:
            raise NotFoundException("Marca", str(command.id))

        await self._repository.delete(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == command.id)
        )
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))
