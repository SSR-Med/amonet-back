from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Marca.GetAllMarcas.dtos import (
    MarcaResponseDto,
)
from Application.Features.Marca.GetAllMarcas.mappers import (
    MarcaMapper,
)
from Application.Features.Marca.GetAllMarcas.query import (
    GetAllMarcasQuery,
)
from Application.Features.Marca.GetAllMarcas.query_builders import (
    MarcaQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllMarcasQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MarcaConfiguration)

    async def handle(
        self, query: GetAllMarcasQuery
    ) -> PaginatedResult[MarcaResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=MarcaQueryBuilder(query).build(),
        )

        return MarcaMapper.to_paginated_response(items, page, total, page_size)
