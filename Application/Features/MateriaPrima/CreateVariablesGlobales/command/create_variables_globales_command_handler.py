from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.CreateVariablesGlobales.command import (
    CreateVariablesGlobalesCommand,
)
from Application.Features.MateriaPrima.CreateVariablesGlobales.mappers import (
    CreateVariablesGlobalesMapper,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateVariablesGlobalesCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, VariablesGlobalesMateriaPrimaConfiguration
        )
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateVariablesGlobalesCommand, current_user: CurrentUserDto
    ) -> VariablesGlobalesMateriaPrimaResponseDto:
        command.nombre = command.nombre.strip().upper()

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.nombre == command.nombre
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Variable global materia prima '{command.nombre}' already exists"
            )

        model = CreateVariablesGlobalesMapper.to_model(command)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return VariablesGlobalesMateriaPrimaMapper.to_response(model)
