from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TagKanban.CreateTagKanban.dtos import (
    TagKanbanResponseDto,
)
from Application.Features.TagKanban.CreateTagKanban.mappers import (
    TagKanbanMapper,
)
from Application.Features.TagKanban.GetAllTagsKanban.query import (
    GetAllTagsKanbanQuery,
)
from Application.Features.TagKanban.GetAllTagsKanban.query_builders import (
    TagKanbanQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import TagKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllTagsKanbanQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TagKanbanConfiguration)

    async def handle(
        self, query: GetAllTagsKanbanQuery
    ) -> PaginatedResult[TagKanbanResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=TagKanbanQueryBuilder(query).build(),
            order_by=TagKanbanConfiguration.nombre.asc(),
        )

        return PaginatedResult(
            items=[TagKanbanMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
