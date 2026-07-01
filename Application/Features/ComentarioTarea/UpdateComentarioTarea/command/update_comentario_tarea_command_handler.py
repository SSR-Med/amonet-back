from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ComentarioTarea.CreateComentarioTarea.dtos import (
    ComentarioTareaResponseDto,
)
from Application.Features.ComentarioTarea.CreateComentarioTarea.mappers import (
    ComentarioTareaMapper,
)
from Application.Features.ComentarioTarea.UpdateComentarioTarea.command import (
    UpdateComentarioTareaCommand,
)
from Application.Features.ComentarioTarea.UpdateComentarioTarea.mappers import (
    UpdateComentarioTareaMapper,
)
from Application.Features.ComentarioTarea.UpdateComentarioTarea.validators import (
    UpdateComentarioTareaValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdateComentarioTareaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ComentarioTareaConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._validator = UpdateComentarioTareaValidator()

    async def handle(
        self, id: UUID, command: UpdateComentarioTareaCommand, current_user: CurrentUserDto
    ) -> ComentarioTareaResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(ComentarioTareaConfiguration.id_amonet_comentario_tarea == id)
        )
        if model is None:
            raise NotFoundException("ComentarioTarea", str(id))

        self._validator.validate(model, current_user)

        model = UpdateComentarioTareaMapper.apply(model, command)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return ComentarioTareaMapper.to_response(model, current_user)
