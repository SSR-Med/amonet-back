from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Producto.GetProductoById.query import (
    GetProductoByIdQuery,
)
from Application.Features.Producto.GetAllProductos.dtos import (
    ProductoResponseDto,
)
from Application.Features.Producto.GetAllProductos.mappers import (
    ProductoLoaderOptions,
    ProductoMapper,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import ProductoConfiguration
from infrastructure.dataaccess.repository import Repository


class GetProductoByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ProductoConfiguration)

    async def handle(self, query: GetProductoByIdQuery) -> ProductoResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.id_amonet_producto == query.id
            ),
            loader_options=ProductoLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("Producto", str(query.id))
        return ProductoMapper.to_response(model)
