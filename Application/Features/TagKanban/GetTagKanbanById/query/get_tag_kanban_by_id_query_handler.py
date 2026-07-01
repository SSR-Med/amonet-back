from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TagKanban.CreateTagKanban.dtos import (
    TagKanbanResponseDto,
)
from Application.Features.TagKanban.CreateTagKanban.mappers import (
    TagKanbanMapper,
)
from Application.Features.TagKanban.GetTagKanbanById.query import (
    GetTagKanbanByIdQuery,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import TagKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class GetTagKanbanByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TagKanbanConfiguration)

    async def handle(self, query: GetTagKanbanByIdQuery) -> TagKanbanResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                TagKanbanConfiguration.id_amonet_tag_kanban == query.id,
                TagKanbanConfiguration.activo == True,
            )
        )
        if model is None:
            raise NotFoundException("TagKanban", str(query.id))

        return TagKanbanMapper.to_response(model)
