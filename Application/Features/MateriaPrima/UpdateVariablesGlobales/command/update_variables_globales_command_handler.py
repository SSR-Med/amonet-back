from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.dtos import (
    UpdateVariablesGlobalesCommandDto,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.mappers import (
    UpdateVariablesGlobalesMapper,
)
from core.exceptions import ConflictException, NotFoundException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class UpdateVariablesGlobalesCommandHandler:

    def __init__(
        self,
        repository: IRepository[VariablesGlobalesMateriaPrimaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(
        self, command: UpdateVariablesGlobalesCommandDto
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
