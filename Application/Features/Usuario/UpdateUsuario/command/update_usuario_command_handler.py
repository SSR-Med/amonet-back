from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.GetAllUsuarios.dtos import (
    UsuarioResponseDto,
)
from Application.Features.Usuario.GetAllUsuarios.mappers import (
    UsuarioMapper,
)
from Application.Features.Usuario.UpdateUsuario.command import (
    UpdateUsuarioCommand,
)
from Application.Features.Usuario.UpdateUsuario.mappers import (
    UpdateUsuarioMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)
from infrastructure.dataaccess.configurations import (
    CatalogoUsuarioRolConfiguration,
    UsuarioConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger, PasswordService


class UpdateUsuarioCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, UsuarioConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._session = session

    async def handle(
        self, id: UUID, command: UpdateUsuarioCommand, current_user: CurrentUserDto
    ) -> UsuarioResponseDto:
        if id == current_user.id:
            raise UnauthorizedException("Cannot modify yourself")

        model = await self._repository.first_or_default(
            lambda q: q.where(UsuarioConfiguration.id_amonet_usuario == id)
        )
        if model is None:
            raise NotFoundException("Usuario", str(id))

        if command.nombre is not None:
            command.nombre = command.nombre.strip().upper()

        if command.documento is not None:
            command.documento = command.documento.strip()
            existing = await self._repository.first_or_default(
                lambda q: q.where(
                    func.upper(func.trim(UsuarioConfiguration.documento))
                    == command.documento.upper(),
                    UsuarioConfiguration.id_amonet_usuario != id,
                )
            )
            if existing is not None:
                raise ConflictException(
                    f"Usuario with documento '{command.documento}' already exists"
                )

        if command.rol is not None:
            command.rol = command.rol.strip().upper()
            result = await self._session.execute(
                select(CatalogoUsuarioRolConfiguration).where(
                    func.upper(CatalogoUsuarioRolConfiguration.nombre)
                    == command.rol
                )
            )
            rol = result.scalar_one_or_none()
            if rol is None:
                raise BadRequestException(f"Rol '{command.rol}' does not exist")

        new_password = (
            PasswordService.hash(command.password)
            if command.password is not None
            else None
        )

        model = UpdateUsuarioMapper.apply(model, command, new_password)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return UsuarioMapper.to_response(model)
