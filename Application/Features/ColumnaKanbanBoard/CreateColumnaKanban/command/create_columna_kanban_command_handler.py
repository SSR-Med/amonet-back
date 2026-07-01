from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.command import (
    CreateColumnaKanbanCommand,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.mappers import (
    ColumnaKanbanMapper,
    CreateColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.validators import (
    CreateColumnaKanbanValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateColumnaKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ColumnaKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._validator = CreateColumnaKanbanValidator(self._repository)

    async def handle(
        self, command: CreateColumnaKanbanCommand, current_user: CurrentUserDto
    ) -> ColumnaKanbanResponseDto:
        command.nombre = command.nombre.strip().upper()

        await self._validator.validate(command.nombre, command.posicion)

        model = CreateColumnaKanbanMapper.to_model(command, current_user.id)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return ColumnaKanbanMapper.to_response(model, current_user)
