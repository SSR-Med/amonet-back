from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.command import (
    UpdateVariablesGlobalesCommand,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.mappers import (
    UpdateVariablesGlobalesMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdateVariablesGlobalesCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, VariablesGlobalesMateriaPrimaConfiguration
        )
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, id: UUID, command: UpdateVariablesGlobalesCommand, current_user: CurrentUserDto
    ) -> VariablesGlobalesMateriaPrimaResponseDto:
        command.nombre = command.nombre.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                == id
            )
        )
        if model is None:
            raise NotFoundException("VariablesGlobalesMateriaPrima", str(id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.nombre == command.nombre,
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                != id,
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Variable global materia prima '{command.nombre}' already exists"
            )

        model = UpdateVariablesGlobalesMapper.apply(model, command)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return VariablesGlobalesMateriaPrimaMapper.to_response(model)
