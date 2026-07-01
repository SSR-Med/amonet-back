from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.DeleteColumnaKanban.command import (
    DeleteColumnaKanbanCommand,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class DeleteColumnaKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ColumnaKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: DeleteColumnaKanbanCommand, current_user: CurrentUserDto
    ) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(ColumnaKanbanConfiguration.id_amonet_columna_kanban == command.id)
        )
        if model is None:
            raise NotFoundException("ColumnaKanban", str(command.id))

        model.activo = False
        model.usuario_modifica = current_user.id
        model.fecha_modifica = datetime.now(timezone.utc)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))
