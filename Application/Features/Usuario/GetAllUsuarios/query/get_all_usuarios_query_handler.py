from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.GetAllUsuarios.dtos import (
    UsuarioResponseDto,
)
from Application.Features.Usuario.GetAllUsuarios.mappers import (
    UsuarioMapper,
)
from Application.Features.Usuario.GetAllUsuarios.query import (
    GetAllUsuariosQuery,
)
from Application.Features.Usuario.GetAllUsuarios.query_builders import (
    UsuarioQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllUsuariosQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, UsuarioConfiguration)

    async def handle(
        self, query: GetAllUsuariosQuery
    ) -> PaginatedResult[UsuarioResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=UsuarioQueryBuilder(query).build(),
        )

        return UsuarioMapper.to_paginated_response(items, page, total, page_size)
