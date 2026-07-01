from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.mappers import (
    ColumnaKanbanLoaderOptions,
    ColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.UpdateColumnaKanban.command import (
    UpdateColumnaKanbanCommand,
)
from Application.Features.ColumnaKanbanBoard.UpdateColumnaKanban.mappers import (
    UpdateColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.UpdateColumnaKanban.validators import (
    UpdateColumnaKanbanValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdateColumnaKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ColumnaKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._validator = UpdateColumnaKanbanValidator(self._repository)

    async def handle(
        self, id: UUID, command: UpdateColumnaKanbanCommand, current_user: CurrentUserDto
    ) -> ColumnaKanbanResponseDto:
        command.nombre = command.nombre.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(ColumnaKanbanConfiguration.id_amonet_columna_kanban == id)
        )
        if model is None:
            raise NotFoundException("ColumnaKanban", str(id))

        await self._validator.validate(command.nombre, command.posicion, id)

        model = UpdateColumnaKanbanMapper.apply(model, command, current_user.id)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        model = await self._repository.first_or_default(
            lambda q: q.where(ColumnaKanbanConfiguration.id_amonet_columna_kanban == id),
            loader_options=ColumnaKanbanLoaderOptions.get(),
        )

        return ColumnaKanbanMapper.to_response(model)
