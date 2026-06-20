from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.GetAllEstadosProduccion.dtos import (
    EstadoProduccionResponseDto,
)
from Application.Features.OrdenProduccion.GetAllEstadosProduccion.mappers import (
    EstadoProduccionMapper,
)
from Application.Features.OrdenProduccion.GetAllEstadosProduccion.query import (
    GetAllEstadosProduccionQuery,
)
from infrastructure.dataaccess.configurations import (
    CatalogoEstadoProduccionConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllEstadosProduccionQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, CatalogoEstadoProduccionConfiguration)

    async def handle(
        self, _query: GetAllEstadosProduccionQuery
    ) -> List[EstadoProduccionResponseDto]:
        items, _, _, _ = await self._repository.get_all(
            page=1,
            page_size=100,
            where=lambda q: q.where(
                CatalogoEstadoProduccionConfiguration.status == True
            ),
        )
        return EstadoProduccionMapper.to_list(items)
