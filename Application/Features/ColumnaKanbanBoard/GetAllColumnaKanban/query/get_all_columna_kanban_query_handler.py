from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.mappers import (
    ColumnaKanbanLoaderOptions,
    ColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.GetAllColumnaKanban.query import (
    GetAllColumnaKanbanQuery,
)
from Application.Features.ColumnaKanbanBoard.GetAllColumnaKanban.query_builders import (
    ColumnaKanbanQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllColumnaKanbanQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ColumnaKanbanConfiguration)

    async def handle(
        self, query: GetAllColumnaKanbanQuery
    ) -> PaginatedResult[ColumnaKanbanResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=ColumnaKanbanQueryBuilder(query).build(),
            loader_options=ColumnaKanbanLoaderOptions.get(),
            order_by=ColumnaKanbanConfiguration.posicion.asc(),
        )

        return PaginatedResult(
            items=[ColumnaKanbanMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
