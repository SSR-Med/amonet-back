from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.dtos import (
    TipoMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.mappers import (
    TipoMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.query import (
    GetAllTiposMateriaPrimaQuery,
)
from infrastructure.dataaccess.configurations import (
    CatalogoTipoMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllTiposMateriaPrimaQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, CatalogoTipoMateriaPrimaConfiguration
        )

    async def handle(
        self, query: GetAllTiposMateriaPrimaQuery
    ) -> List[TipoMateriaPrimaResponseDto]:
        items, _, _, _ = await self._repository.get_all(
            page=1,
            page_size=100,
            where=lambda q: q.where(
                CatalogoTipoMateriaPrimaConfiguration.status == True
            ),
        )
        return TipoMateriaPrimaMapper.to_list(items)
