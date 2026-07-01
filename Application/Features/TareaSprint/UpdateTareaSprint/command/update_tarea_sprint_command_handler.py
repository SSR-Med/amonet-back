from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TareaSprint.CreateTareaSprint.dtos import (
    TareaSprintResponseDto,
)
from Application.Features.TareaSprint.CreateTareaSprint.mappers import (
    TareaSprintLoaderOptions,
    TareaSprintMapper,
)
from Application.Features.TareaSprint.UpdateTareaSprint.command import (
    UpdateTareaSprintCommand,
)
from Application.Features.TareaSprint.UpdateTareaSprint.mappers import (
    UpdateTareaSprintMapper,
)
from Application.Features.TareaSprint.UpdateTareaSprint.validators import (
    UpdateTareaSprintValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    ColumnaKanbanConfiguration,
    PrioridadKanbanConfiguration,
    SprintConfiguration,
    TagKanbanConfiguration,
    TareaSprintConfiguration,
    UsuarioConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdateTareaSprintCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TareaSprintConfiguration)
        self._session = session
        self._unit_of_work = UnitOfWork(session)
        self._validator = UpdateTareaSprintValidator(
            sprint_repository=Repository(session, SprintConfiguration),
            columna_repository=Repository(session, ColumnaKanbanConfiguration),
            usuario_repository=Repository(session, UsuarioConfiguration),
            prioridad_repository=Repository(session, PrioridadKanbanConfiguration),
            tag_repository=Repository(session, TagKanbanConfiguration),
        )

    async def handle(
        self, id: UUID, command: UpdateTareaSprintCommand, current_user: CurrentUserDto
    ) -> TareaSprintResponseDto:
        command.titulo = command.titulo.strip().upper()
        command.descripcion = command.descripcion.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(TareaSprintConfiguration.id_amonet_tarea_sprint == id)
        )
        if model is None:
            raise NotFoundException("TareaSprint", str(id))

        await self._validator.validate(
            command.amonet_sprint_id, command.amonet_columna_kanban_id, command.asignado, command.amonet_prioridad_kanban_id, command.tags
        )

        model = UpdateTareaSprintMapper.apply(model, command, current_user.id)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        model = await self._repository.first_or_default(
            lambda q: q.where(TareaSprintConfiguration.id_amonet_tarea_sprint == id),
            loader_options=TareaSprintLoaderOptions.get(),
        )

        tag_lookup = await TareaSprintMapper.build_tag_lookup(self._session, command.tags or [])
        prioridad_lookup = await TareaSprintMapper.build_prioridad_lookup(self._session, command.amonet_prioridad_kanban_id)
        return TareaSprintMapper.to_response(model, tag_lookup=tag_lookup, prioridad_lookup=prioridad_lookup)
