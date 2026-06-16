from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Inventario.GetInventarioById.query import (
    GetInventarioByIdQuery,
)
from Application.Features.Inventario.GetAllInventario.dtos import (
    InventarioResponseDto,
)
from Application.Features.Inventario.GetAllInventario.mappers import (
    InventarioLoaderOptions,
    InventarioMapper,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetInventarioByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, InventarioMateriaPrimaConfiguration)

    async def handle(self, query: GetInventarioByIdQuery) -> InventarioResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                InventarioMateriaPrimaConfiguration.id_amonet_inventario_materia_prima == query.id
            ),
            loader_options=InventarioLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("Inventario", str(query.id))
        return InventarioMapper.to_response(model)
