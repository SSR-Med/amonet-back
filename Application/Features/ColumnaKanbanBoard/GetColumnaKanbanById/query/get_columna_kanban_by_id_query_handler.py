from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.mappers import (
    ColumnaKanbanLoaderOptions,
    ColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.GetColumnaKanbanById.query import (
    GetColumnaKanbanByIdQuery,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class GetColumnaKanbanByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ColumnaKanbanConfiguration)

    async def handle(
        self, query: GetColumnaKanbanByIdQuery
    ) -> ColumnaKanbanResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(ColumnaKanbanConfiguration.id_amonet_columna_kanban == query.id),
            loader_options=ColumnaKanbanLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("ColumnaKanban", str(query.id))

        return ColumnaKanbanMapper.to_response(model)
