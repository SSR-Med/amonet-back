from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.dtos import (
    OrdenProduccionResponseDto,
)
from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.mappers import (
    OrdenProduccionLoaderOptions,
    OrdenProduccionMapper,
)
from Application.Features.OrdenProduccion.GetOrdenProduccionById.query import (
    GetOrdenProduccionByIdQuery,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import OrdenProduccionConfiguration
from infrastructure.dataaccess.repository import Repository


class GetOrdenProduccionByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, OrdenProduccionConfiguration)

    async def handle(
        self, query: GetOrdenProduccionByIdQuery
    ) -> OrdenProduccionResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                OrdenProduccionConfiguration.id_amonet_orden_produccion == query.id
            ),
            loader_options=OrdenProduccionLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("OrdenProduccion", str(query.id))

        return OrdenProduccionMapper.to_response(model)
