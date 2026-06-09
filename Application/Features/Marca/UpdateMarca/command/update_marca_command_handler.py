from uuid import UUID

from Application.Features.Marca.GetAllMarcas.dtos import (
    MarcaResponseDto,
)
from Application.Features.Marca.GetAllMarcas.mappers import (
    MarcaMapper,
)
from Application.Features.Marca.UpdateMarca.dtos import (
    UpdateMarcaCommandDto,
)
from Application.Features.Marca.UpdateMarca.mappers import (
    UpdateMarcaMapper,
)
from core.exceptions import ConflictException, NotFoundException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import MarcaConfiguration


class UpdateMarcaCommandHandler:

    def __init__(
        self,
        repository: IRepository[MarcaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(
        self, id: UUID, dto: UpdateMarcaCommandDto
    ) -> MarcaResponseDto:
        dto.nombre = dto.nombre.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == id)
        )
        if model is None:
            raise NotFoundException("Marca", str(id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                MarcaConfiguration.nombre == dto.nombre,
                MarcaConfiguration.id_amonet_marca != id,
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Marca '{dto.nombre}' already exists"
            )

        model = UpdateMarcaMapper.apply(model, dto)
        await self._repository.update(model)
        await self._unit_of_work.commit()
        return MarcaMapper.to_response(model)
