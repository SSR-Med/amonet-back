from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Inventario.GetAllInventario.dtos import (
    InventarioResponseDto,
)
from Application.Features.Inventario.GetAllInventario.mappers import (
    InventarioLoaderOptions,
    InventarioMapper,
)
from Application.Features.Inventario.GetAllInventario.query import (
    GetAllInventarioQuery,
)
from Application.Features.Inventario.GetAllInventario.query_builders import (
    InventarioQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllInventarioQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, InventarioMateriaPrimaConfiguration)

    async def handle(
        self, query: GetAllInventarioQuery
    ) -> PaginatedResult[InventarioResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=InventarioQueryBuilder(query).build(),
            loader_options=InventarioLoaderOptions.get(),
        )

        return InventarioMapper.to_paginated_response(items, page, total, page_size)
