from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ComentarioTarea.CreateComentarioTarea.command import (
    CreateComentarioTareaCommand,
)
from Application.Features.ComentarioTarea.CreateComentarioTarea.dtos import (
    ComentarioTareaResponseDto,
)
from Application.Features.ComentarioTarea.CreateComentarioTarea.mappers import (
    ComentarioTareaMapper,
    CreateComentarioTareaMapper,
)
from Application.Features.ComentarioTarea.CreateComentarioTarea.validators import (
    CreateComentarioTareaValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from infrastructure.dataaccess.configurations import (
    ComentarioTareaConfiguration,
    TareaSprintConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateComentarioTareaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ComentarioTareaConfiguration)
        self._tarea_repository = Repository(session, TareaSprintConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._validator = CreateComentarioTareaValidator(self._tarea_repository)

    async def handle(
        self, command: CreateComentarioTareaCommand, current_user: CurrentUserDto
    ) -> ComentarioTareaResponseDto:
        await self._validator.validate(command.amonet_tarea_sprint_id)

        model = CreateComentarioTareaMapper.to_model(command, current_user.id)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return ComentarioTareaMapper.to_response(model, current_user)
