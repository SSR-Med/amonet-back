from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.DeleteMateriaPrima.command import (
    DeleteMateriaPrimaCommand,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class DeleteMateriaPrimaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MateriaPrimaConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(self, command: DeleteMateriaPrimaCommand, current_user: CurrentUserDto) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                MateriaPrimaConfiguration.id_amonet_materia_prima == command.id
            )
        )
        if model is None:
            raise NotFoundException("MateriaPrima", str(command.id))

        model.status = False
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))
