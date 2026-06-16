from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetMateriaPrimaById.query import (
    GetMateriaPrimaByIdQuery,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos import (
    MateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.mappers import (
    MateriaPrimaLoaderOptions,
    MateriaPrimaMapper,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import MateriaPrimaConfiguration
from infrastructure.dataaccess.repository import Repository


class GetMateriaPrimaByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MateriaPrimaConfiguration)

    async def handle(self, query: GetMateriaPrimaByIdQuery) -> MateriaPrimaResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                MateriaPrimaConfiguration.id_amonet_materia_prima == query.id
            ),
            loader_options=MateriaPrimaLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("MateriaPrima", str(query.id))
        return MateriaPrimaMapper.to_response(model)
