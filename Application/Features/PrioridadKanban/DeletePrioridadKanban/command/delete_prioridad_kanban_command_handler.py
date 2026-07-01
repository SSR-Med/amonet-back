from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.PrioridadKanban.DeletePrioridadKanban.command import (
    DeletePrioridadKanbanCommand,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class DeletePrioridadKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, PrioridadKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: DeletePrioridadKanbanCommand, current_user: CurrentUserDto
    ) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(PrioridadKanbanConfiguration.id_amonet_prioridad_kanban == command.id)
        )
        if model is None:
            raise NotFoundException("PrioridadKanban", str(command.id))

        model.activo = False
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))
