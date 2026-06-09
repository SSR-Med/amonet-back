from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Marca.GetAllMarcas.dtos import (
    MarcaResponseDto,
)
from Application.Features.Marca.GetAllMarcas.mappers import (
    MarcaMapper,
)
from Application.Features.Marca.UpdateMarca.command import (
    UpdateMarcaCommand,
)
from Application.Features.Marca.UpdateMarca.mappers import (
    UpdateMarcaMapper,
)
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class UpdateMarcaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MarcaConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: UpdateMarcaCommand
    ) -> MarcaResponseDto:
        command.nombre = command.nombre.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == command.id)
        )
        if model is None:
            raise NotFoundException("Marca", str(command.id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                MarcaConfiguration.nombre == command.nombre,
                MarcaConfiguration.id_amonet_marca != command.id,
            )
        )
        if existing is not None:
            raise ConflictException(f"Marca '{command.nombre}' already exists")

        model = UpdateMarcaMapper.apply(model, command)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        return MarcaMapper.to_response(model)
