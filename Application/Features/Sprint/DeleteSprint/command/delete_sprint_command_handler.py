from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Sprint.DeleteSprint.command import (
    DeleteSprintCommand,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import SprintConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class DeleteSprintCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, SprintConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: DeleteSprintCommand, current_user: CurrentUserDto
    ) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(SprintConfiguration.id_amonet_sprint == command.id)
        )
        if model is None:
            raise NotFoundException("Sprint", str(command.id))

        model.activo = False
        model.principal = False
        model.usuario_modifica = current_user.id
        model.fecha_modifica = datetime.now(timezone.utc)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))
