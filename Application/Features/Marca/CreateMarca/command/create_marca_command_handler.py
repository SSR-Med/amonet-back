from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Marca.CreateMarca.command import (
    CreateMarcaCommand,
)
from Application.Features.Marca.CreateMarca.mappers import (
    CreateMarcaMapper,
)
from Application.Features.Marca.GetAllMarcas.dtos import (
    MarcaResponseDto,
)
from Application.Features.Marca.GetAllMarcas.mappers import (
    MarcaMapper,
)
from core.dtos import CurrentUserDto
from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger
from core.dtos import AuditLogDto


class CreateMarcaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MarcaConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateMarcaCommand, current_user: CurrentUserDto
    ) -> MarcaResponseDto:
        command.nombre = command.nombre.strip().upper()

        existing = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.nombre == command.nombre)
        )
        if existing is not None:
            raise ConflictException(f"Marca '{command.nombre}' already exists")

        model = CreateMarcaMapper.to_model(command)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return MarcaMapper.to_response(model)
