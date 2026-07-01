from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Sprint.CreateSprint.command import (
    CreateSprintCommand,
)
from Application.Features.Sprint.CreateSprint.dtos import (
    SprintResponseDto,
)
from Application.Features.Sprint.CreateSprint.mappers import (
    CreateSprintMapper,
    SprintMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from infrastructure.dataaccess.configurations import SprintConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateSprintCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, SprintConfiguration)
        self._session = session
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateSprintCommand, current_user: CurrentUserDto
    ) -> SprintResponseDto:
        await self._session.execute(
            update(SprintConfiguration).values(principal=False)
        )

        model = CreateSprintMapper.to_model(
            command, current_user.id, datetime.now(timezone.utc)
        )
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return SprintMapper.to_response(model, current_user)
