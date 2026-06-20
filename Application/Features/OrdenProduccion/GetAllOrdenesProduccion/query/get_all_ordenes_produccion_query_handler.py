from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.dtos import (
    OrdenProduccionResponseDto,
)
from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.mappers import (
    OrdenProduccionLoaderOptions,
    OrdenProduccionMapper,
)
from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.query import (
    GetAllOrdenesProduccionQuery,
)
from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.query_builders import (
    OrdenProduccionQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import OrdenProduccionConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllOrdenesProduccionQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, OrdenProduccionConfiguration)

    async def handle(
        self, query: GetAllOrdenesProduccionQuery
    ) -> PaginatedResult[OrdenProduccionResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=OrdenProduccionQueryBuilder(query).build(),
            loader_options=OrdenProduccionLoaderOptions.get(),
            order_by=OrdenProduccionConfiguration.fecha_alta.desc(),
        )

        return OrdenProduccionMapper.to_paginated_response(items, page, total, page_size)
