from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ComentarioTarea.DeleteComentarioTarea.command import (
    DeleteComentarioTareaCommand,
)
from core.constants import ADMIN
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException, UnauthorizedException
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class DeleteComentarioTareaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ComentarioTareaConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: DeleteComentarioTareaCommand, current_user: CurrentUserDto
    ) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(ComentarioTareaConfiguration.id_amonet_comentario_tarea == command.id)
        )
        if model is None:
            raise NotFoundException("ComentarioTarea", str(command.id))

        if model.usuario_alta != current_user.id and current_user.rol != ADMIN:
            raise UnauthorizedException("You can only delete your own comments")

        model.activo = False
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))
