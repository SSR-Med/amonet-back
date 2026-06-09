from typing import List

from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.dtos import (
    GetAllTiposMateriaPrimaQuery,
    TipoMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.mappers import (
    TipoMateriaPrimaMapper,
)
from core.interfaces import IRepository
from infrastructure.dataaccess.configurations import (
    CatalogoTipoMateriaPrimaConfiguration,
)


class GetAllTiposMateriaPrimaQueryHandler:

    def __init__(
        self,
        repository: IRepository[CatalogoTipoMateriaPrimaConfiguration],
    ) -> None:
        self._repository = repository

    async def handle(
        self, query: GetAllTiposMateriaPrimaQuery
    ) -> List[TipoMateriaPrimaResponseDto]:
        items, _, _, _ = await self._repository.get_all(page=1, page_size=100)
        return TipoMateriaPrimaMapper.to_list(items)
