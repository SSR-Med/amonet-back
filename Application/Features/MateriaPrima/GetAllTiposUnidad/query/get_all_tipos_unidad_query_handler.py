from typing import List

from Application.Features.MateriaPrima.GetAllTiposUnidad.dtos import (
    TipoUnidadResponseDto,
)
from Application.Features.MateriaPrima.GetAllTiposUnidad.mappers import (
    TipoUnidadMapper,
)
from core.interfaces import IRepository
from infrastructure.dataaccess.configurations import (
    CatalogoTipoUnidadConfiguration,
)


class GetAllTiposUnidadQueryHandler:

    def __init__(
        self,
        repository: IRepository[CatalogoTipoUnidadConfiguration],
    ) -> None:
        self._repository = repository

    async def handle(self) -> List[TipoUnidadResponseDto]:
        items, _, _, _ = await self._repository.get_all(page=1, page_size=100)
        return TipoUnidadMapper.to_list(items)
