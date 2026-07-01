from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TagKanban.CreateTagKanban.command import (
    CreateTagKanbanCommand,
)
from Application.Features.TagKanban.CreateTagKanban.dtos import (
    TagKanbanResponseDto,
)
from Application.Features.TagKanban.CreateTagKanban.mappers import (
    CreateTagKanbanMapper,
    TagKanbanMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import BadRequestException, ConflictException
from infrastructure.dataaccess.configurations import TagKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateTagKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TagKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateTagKanbanCommand, current_user: CurrentUserDto
    ) -> TagKanbanResponseDto:
        command.nombre = command.nombre.strip().upper()

        for val, name in [
            (command.color_red, "red"),
            (command.color_green, "green"),
            (command.color_blue, "blue"),
        ]:
            if val < 0 or val > 255:
                raise BadRequestException(f"color_{name} must be between 0 and 255")

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                TagKanbanConfiguration.color_red == command.color_red,
                TagKanbanConfiguration.color_green == command.color_green,
                TagKanbanConfiguration.color_blue == command.color_blue,
            )
        )
        if existing is not None:
            raise ConflictException("Color combination already exists")

        existing = await self._repository.first_or_default(
            lambda q: q.where(TagKanbanConfiguration.nombre == command.nombre)
        )
        if existing is not None:
            raise ConflictException(f"TagKanban '{command.nombre}' already exists")

        model = CreateTagKanbanMapper.to_model(command)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return TagKanbanMapper.to_response(model)
