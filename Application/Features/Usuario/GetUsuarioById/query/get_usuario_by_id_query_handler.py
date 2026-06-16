from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.GetUsuarioById.query import GetUsuarioByIdQuery
from Application.Features.Usuario.GetAllUsuarios.dtos import UsuarioResponseDto
from Application.Features.Usuario.GetAllUsuarios.mappers import UsuarioMapper
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.dataaccess.repository import Repository


class GetUsuarioByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, UsuarioConfiguration)

    async def handle(self, query: GetUsuarioByIdQuery) -> UsuarioResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(UsuarioConfiguration.id_amonet_usuario == query.id)
        )
        if model is None:
            raise NotFoundException("Usuario", str(query.id))
        return UsuarioMapper.to_response(model)
