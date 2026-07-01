from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.PrioridadKanban.CreatePrioridadKanban.dtos import (
    PrioridadKanbanResponseDto,
)
from Application.Features.PrioridadKanban.CreatePrioridadKanban.mappers import (
    PrioridadKanbanMapper,
)
from Application.Features.PrioridadKanban.GetPrioridadKanbanById.query import (
    GetPrioridadKanbanByIdQuery,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class GetPrioridadKanbanByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, PrioridadKanbanConfiguration)

    async def handle(self, query: GetPrioridadKanbanByIdQuery) -> PrioridadKanbanResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                PrioridadKanbanConfiguration.id_amonet_prioridad_kanban == query.id,
                PrioridadKanbanConfiguration.activo == True,
            )
        )
        if model is None:
            raise NotFoundException("PrioridadKanban", str(query.id))

        return PrioridadKanbanMapper.to_response(model)
