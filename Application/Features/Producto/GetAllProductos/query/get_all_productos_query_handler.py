from sqlalchemy.orm import selectinload

from Application.Features.Producto.GetAllProductos.query import (
    GetAllProductosQuery,
)
from Application.Features.Producto.GetAllProductos.dtos import (
    ProductoResponseDto,
)
from Application.Features.Producto.GetAllProductos.mappers import (
    ProductoMapper,
)
from Application.Features.Producto.GetAllProductos.query_builders import (
    ProductoQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    ProductoConfiguration,
    ProductoMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllProductosQueryHandler:

    def __init__(self, session) -> None:
        self._repository = Repository(session, ProductoConfiguration)

    async def handle(
        self, query: GetAllProductosQuery
    ) -> PaginatedResult[ProductoResponseDto]:
        loader_options = [
            selectinload(ProductoConfiguration.marca),
            selectinload(ProductoConfiguration.materias_primas).selectinload(
                ProductoMateriaPrimaConfiguration.materia_prima
            ),
        ]

        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=ProductoQueryBuilder(query).build(),
            loader_options=loader_options,
        )

        return PaginatedResult(
            items=[ProductoMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
