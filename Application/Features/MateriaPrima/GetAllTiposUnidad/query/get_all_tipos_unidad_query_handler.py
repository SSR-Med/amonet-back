from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllTiposUnidad.dtos import (
    TipoUnidadResponseDto,
)
from Application.Features.MateriaPrima.GetAllTiposUnidad.mappers import (
    TipoUnidadMapper,
)
from Application.Features.MateriaPrima.GetAllTiposUnidad.query import (
    GetAllTiposUnidadQuery,
)
from infrastructure.dataaccess.configurations import (
    CatalogoTipoUnidadConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllTiposUnidadQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, CatalogoTipoUnidadConfiguration)

    async def handle(
        self, query: GetAllTiposUnidadQuery
    ) -> List[TipoUnidadResponseDto]:
        items, _, _, _ = await self._repository.get_all(
            page=1,
            page_size=100,
            where=lambda q: q.where(
                CatalogoTipoUnidadConfiguration.status == True
            ),
        )
        return TipoUnidadMapper.to_list(items)
