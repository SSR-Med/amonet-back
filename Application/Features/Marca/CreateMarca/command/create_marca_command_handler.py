from Application.Features.Marca.CreateMarca.dtos import (
    CreateMarcaCommandDto,
)
from Application.Features.Marca.CreateMarca.mappers import (
    CreateMarcaMapper,
)
from Application.Features.Marca.GetAllMarcas.mappers import (
    MarcaMapper,
)
from Application.Features.Marca.GetAllMarcas.dtos import (
    MarcaResponseDto,
)
from core.exceptions import ConflictException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import MarcaConfiguration


class CreateMarcaCommandHandler:

    def __init__(
        self,
        repository: IRepository[MarcaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(
        self, dto: CreateMarcaCommandDto
    ) -> MarcaResponseDto:
        dto.nombre = dto.nombre.strip().upper()

        existing = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.nombre == dto.nombre)
        )
        if existing is not None:
            raise ConflictException(
                f"Marca '{dto.nombre}' already exists"
            )

        model = CreateMarcaMapper.to_model(dto)
        await self._repository.create(model)
        await self._unit_of_work.commit()
        return MarcaMapper.to_response(model)
