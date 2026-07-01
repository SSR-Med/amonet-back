from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.PrioridadKanban.CreatePrioridadKanban.dtos import (
    PrioridadKanbanResponseDto,
)
from Application.Features.PrioridadKanban.CreatePrioridadKanban.mappers import (
    PrioridadKanbanMapper,
)
from Application.Features.PrioridadKanban.UpdatePrioridadKanban.command import (
    UpdatePrioridadKanbanCommand,
)
from Application.Features.PrioridadKanban.UpdatePrioridadKanban.mappers import (
    UpdatePrioridadKanbanMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import BadRequestException, ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdatePrioridadKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, PrioridadKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, id: UUID, command: UpdatePrioridadKanbanCommand, current_user: CurrentUserDto
    ) -> PrioridadKanbanResponseDto:
        command.nombre = command.nombre.strip().upper()

        for val, name in [
            (command.color_red, "red"),
            (command.color_green, "green"),
            (command.color_blue, "blue"),
        ]:
            if val < 0 or val > 255:
                raise BadRequestException(f"color_{name} must be between 0 and 255")

        existing_color = await self._repository.first_or_default(
            lambda q: q.where(
                PrioridadKanbanConfiguration.color_red == command.color_red,
                PrioridadKanbanConfiguration.color_green == command.color_green,
                PrioridadKanbanConfiguration.color_blue == command.color_blue,
                PrioridadKanbanConfiguration.id_amonet_prioridad_kanban != id,
            )
        )
        if existing_color is not None:
            raise ConflictException("Color combination already exists")

        model = await self._repository.first_or_default(
            lambda q: q.where(PrioridadKanbanConfiguration.id_amonet_prioridad_kanban == id)
        )
        if model is None:
            raise NotFoundException("PrioridadKanban", str(id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                PrioridadKanbanConfiguration.nombre == command.nombre,
                PrioridadKanbanConfiguration.id_amonet_prioridad_kanban != id,
            )
        )
        if existing is not None:
            raise ConflictException(f"PrioridadKanban '{command.nombre}' already exists")

        model = UpdatePrioridadKanbanMapper.apply(model, command)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return PrioridadKanbanMapper.to_response(model)
