from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Sprint.CreateSprint.dtos import (
    SprintResponseDto,
)
from Application.Features.Sprint.CreateSprint.mappers import (
    SprintLoaderOptions,
    SprintMapper,
)
from Application.Features.Sprint.GetAllSprints.query import (
    GetAllSprintsQuery,
)
from Application.Features.Sprint.GetAllSprints.query_builders import (
    SprintQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import SprintConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllSprintsQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, SprintConfiguration)

    async def handle(
        self, query: GetAllSprintsQuery
    ) -> PaginatedResult[SprintResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=SprintQueryBuilder(query).build(),
            loader_options=SprintLoaderOptions.get(),
            order_by=SprintConfiguration.contador.desc(),
        )

        return PaginatedResult(
            items=[SprintMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
