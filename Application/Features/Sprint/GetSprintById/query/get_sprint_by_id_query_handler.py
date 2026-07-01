from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Sprint.CreateSprint.dtos import (
    SprintResponseDto,
)
from Application.Features.Sprint.CreateSprint.mappers import (
    SprintLoaderOptions,
    SprintMapper,
)
from Application.Features.Sprint.GetSprintById.query import (
    GetSprintByIdQuery,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import SprintConfiguration
from infrastructure.dataaccess.repository import Repository


class GetSprintByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, SprintConfiguration)

    async def handle(self, query: GetSprintByIdQuery) -> SprintResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                SprintConfiguration.id_amonet_sprint == query.id,
                SprintConfiguration.activo == True,
            ),
            loader_options=SprintLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("Sprint", str(query.id))

        return SprintMapper.to_response(model)
