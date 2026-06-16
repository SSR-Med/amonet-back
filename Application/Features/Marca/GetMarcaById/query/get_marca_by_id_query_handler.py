from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Marca.GetMarcaById.query import GetMarcaByIdQuery
from Application.Features.Marca.GetAllMarcas.dtos import MarcaResponseDto
from Application.Features.Marca.GetAllMarcas.mappers import MarcaMapper
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.dataaccess.repository import Repository


class GetMarcaByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MarcaConfiguration)

    async def handle(self, query: GetMarcaByIdQuery) -> MarcaResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == query.id)
        )
        if model is None:
            raise NotFoundException("Marca", str(query.id))
        return MarcaMapper.to_response(model)
