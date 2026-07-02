from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Sprint.CreateSprint.dtos import (
    SprintResponseDto,
)
from Application.Features.Sprint.CreateSprint.mappers import (
    SprintLoaderOptions,
    SprintMapper,
)
from Application.Features.Sprint.UpdateSprint.command import (
    UpdateSprintCommand,
)
from Application.Features.Sprint.UpdateSprint.mappers import (
    UpdateSprintMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import SprintConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdateSprintCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, SprintConfiguration)
        self._session = session
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, id: UUID, command: UpdateSprintCommand, current_user: CurrentUserDto
    ) -> SprintResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(SprintConfiguration.id_amonet_sprint == id)
        )
        if model is None:
            raise NotFoundException("Sprint", str(id))

        if command.principal is True:
            await self._session.execute(
                update(SprintConfiguration).values(
                    principal=False,
                    fecha_fin=datetime.now(timezone.utc),
                )
            )

        model = UpdateSprintMapper.apply(model, command, current_user.id)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        model = await self._repository.first_or_default(
            lambda q: q.where(SprintConfiguration.id_amonet_sprint == id),
            loader_options=SprintLoaderOptions.get(),
        )

        return SprintMapper.to_response(model)
