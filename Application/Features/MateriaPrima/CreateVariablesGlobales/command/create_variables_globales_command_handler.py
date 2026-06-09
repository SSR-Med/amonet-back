from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.CreateVariablesGlobales.dtos import (
    CreateVariablesGlobalesCommandDto,
)
from Application.Features.MateriaPrima.CreateVariablesGlobales.mappers import (
    CreateVariablesGlobalesMapper,
)
from core.exceptions import ConflictException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class CreateVariablesGlobalesCommandHandler:

    def __init__(
        self,
        repository: IRepository[VariablesGlobalesMateriaPrimaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(
        self, dto: CreateVariablesGlobalesCommandDto
    ) -> VariablesGlobalesMateriaPrimaResponseDto:
        dto.nombre = dto.nombre.strip().upper()

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.nombre == dto.nombre
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Variable global materia prima '{dto.nombre}' already exists"
            )

        model = CreateVariablesGlobalesMapper.to_model(dto)
        await self._repository.create(model)
        await self._unit_of_work.commit()
        return VariablesGlobalesMateriaPrimaMapper.to_response(model)
