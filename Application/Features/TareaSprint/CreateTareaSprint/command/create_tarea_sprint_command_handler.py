from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TareaSprint.CreateTareaSprint.command import (
    CreateTareaSprintCommand,
)
from Application.Features.TareaSprint.CreateTareaSprint.dtos import (
    TareaSprintResponseDto,
)
from Application.Features.TareaSprint.CreateTareaSprint.mappers import (
    CreateTareaSprintMapper,
    TareaSprintMapper,
)
from Application.Features.TareaSprint.CreateTareaSprint.validators import (
    CreateTareaSprintValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
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


class CreateTareaSprintCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TareaSprintConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._session = session
        self._validator = CreateTareaSprintValidator(
            sprint_repository=Repository(session, SprintConfiguration),
            columna_repository=Repository(session, ColumnaKanbanConfiguration),
            usuario_repository=Repository(session, UsuarioConfiguration),
            prioridad_repository=Repository(session, PrioridadKanbanConfiguration),
            tag_repository=Repository(session, TagKanbanConfiguration),
        )

    async def handle(
        self, command: CreateTareaSprintCommand, current_user: CurrentUserDto
    ) -> TareaSprintResponseDto:
        command.titulo = command.titulo.strip().upper()
        command.descripcion = command.descripcion.strip().upper()

        await self._validator.validate(
            command.amonet_sprint_id, command.amonet_columna_kanban_id, command.asignado, command.amonet_prioridad_kanban_id, command.tags
        )

        model = CreateTareaSprintMapper.to_model(command, current_user.id)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        tag_lookup = await TareaSprintMapper.build_tag_lookup(self._session, command.tags or [])
        prioridad_lookup = await TareaSprintMapper.build_prioridad_lookup(self._session, command.amonet_prioridad_kanban_id)
        return TareaSprintMapper.to_response(model, current_user, tag_lookup=tag_lookup, prioridad_lookup=prioridad_lookup)
