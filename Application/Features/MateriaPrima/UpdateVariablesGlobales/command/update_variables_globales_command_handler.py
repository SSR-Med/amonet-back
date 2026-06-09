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
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class UpdateVariablesGlobalesCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, VariablesGlobalesMateriaPrimaConfiguration
        )
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: UpdateVariablesGlobalesCommand
    ) -> VariablesGlobalesMateriaPrimaResponseDto:
        command.nombre = command.nombre.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                == command.id
            )
        )
        if model is None:
            raise NotFoundException("VariablesGlobalesMateriaPrima", str(command.id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.nombre == command.nombre,
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                != command.id,
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Variable global materia prima '{command.nombre}' already exists"
            )

        model = UpdateVariablesGlobalesMapper.apply(model, command)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        return VariablesGlobalesMateriaPrimaMapper.to_response(model)
