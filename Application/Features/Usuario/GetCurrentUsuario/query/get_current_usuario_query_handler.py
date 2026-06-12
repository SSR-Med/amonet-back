from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.GetCurrentUsuario.dtos import (
    CurrentUsuarioResponseDto,
)
from Application.Features.Usuario.GetCurrentUsuario.mappers import (
    CurrentUsuarioMapper,
)
from Application.Features.Usuario.GetCurrentUsuario.query import (
    GetCurrentUsuarioQuery,
)
from core.dtos import CurrentUserDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import UsuarioConfiguration


class GetCurrentUsuarioQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def handle(
        self, query: GetCurrentUsuarioQuery, current_user: CurrentUserDto
    ) -> CurrentUsuarioResponseDto:
        result = await self._session.execute(
            select(UsuarioConfiguration).where(
                UsuarioConfiguration.id_amonet_usuario == current_user.id
            )
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise NotFoundException("Usuario", str(current_user.id))

        return CurrentUsuarioMapper.to_response(user)
