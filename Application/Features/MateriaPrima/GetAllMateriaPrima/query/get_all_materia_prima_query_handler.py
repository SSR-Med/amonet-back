from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos import (
    MateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.mappers import (
    MateriaPrimaLoaderOptions,
    MateriaPrimaMapper,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.query import (
    GetAllMateriaPrimaQuery,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.query_builders import (
    MateriaPrimaQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllMateriaPrimaQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MateriaPrimaConfiguration)

    async def handle(
        self, query: GetAllMateriaPrimaQuery
    ) -> PaginatedResult[MateriaPrimaResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=MateriaPrimaQueryBuilder(query).build(),
            loader_options=MateriaPrimaLoaderOptions.get(),
        )

        return MateriaPrimaMapper.to_paginated_response(
            items, page, total, page_size
        )
