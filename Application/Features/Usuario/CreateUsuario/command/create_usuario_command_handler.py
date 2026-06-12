from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.CreateUsuario.command import (
    CreateUsuarioCommand,
)
from Application.Features.Usuario.CreateUsuario.mappers import (
    CreateUsuarioMapper,
)
from Application.Features.Usuario.GetAllUsuarios.dtos import (
    UsuarioResponseDto,
)
from Application.Features.Usuario.GetAllUsuarios.mappers import (
    UsuarioMapper,
)
from core.exceptions import BadRequestException, ConflictException
from infrastructure.dataaccess.configurations import (
    CatalogoUsuarioRolConfiguration,
    UsuarioConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class CreateUsuarioCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, UsuarioConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._session = session

    async def handle(
        self, command: CreateUsuarioCommand
    ) -> UsuarioResponseDto:
        command.nombre = command.nombre.strip().upper()
        command.documento = command.documento.strip()

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                func.upper(func.trim(UsuarioConfiguration.documento))
                == command.documento.upper()
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Usuario with documento '{command.documento}' already exists"
            )

        result = await self._session.execute(
            select(CatalogoUsuarioRolConfiguration).where(
                func.upper(CatalogoUsuarioRolConfiguration.nombre)
                == command.rol.strip().upper()
            )
        )
        rol = result.scalar_one_or_none()
        if rol is None:
            raise BadRequestException(f"Rol '{command.rol}' does not exist")

        model = CreateUsuarioMapper.to_model(command)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        return UsuarioMapper.to_response(model)
