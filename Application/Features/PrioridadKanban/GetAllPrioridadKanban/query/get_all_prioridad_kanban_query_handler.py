from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.PrioridadKanban.CreatePrioridadKanban.dtos import (
    PrioridadKanbanResponseDto,
)
from Application.Features.PrioridadKanban.CreatePrioridadKanban.mappers import (
    PrioridadKanbanMapper,
)
from Application.Features.PrioridadKanban.GetAllPrioridadKanban.query import (
    GetAllPrioridadKanbanQuery,
)
from Application.Features.PrioridadKanban.GetAllPrioridadKanban.query_builders import (
    PrioridadKanbanQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllPrioridadKanbanQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, PrioridadKanbanConfiguration)

    async def handle(
        self, query: GetAllPrioridadKanbanQuery
    ) -> PaginatedResult[PrioridadKanbanResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=PrioridadKanbanQueryBuilder(query).build(),
            order_by=PrioridadKanbanConfiguration.nombre.asc(),
        )

        return PaginatedResult(
            items=[PrioridadKanbanMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
