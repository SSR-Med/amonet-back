from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ComentarioTarea.CreateComentarioTarea.dtos import (
    ComentarioTareaResponseDto,
)
from Application.Features.ComentarioTarea.CreateComentarioTarea.mappers import (
    ComentarioTareaLoaderOptions,
    ComentarioTareaMapper,
)
from Application.Features.ComentarioTarea.GetAllComentariosByTarea.query import (
    GetAllComentariosByTareaQuery,
)
from infrastructure.dataaccess.configurations import ComentarioTareaConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllComentariosByTareaQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ComentarioTareaConfiguration)

    async def handle(
        self, query: GetAllComentariosByTareaQuery
    ) -> List[ComentarioTareaResponseDto]:
        items, _, _, _ = await self._repository.get_all(
            page=1,
            page_size=999999,
            where=lambda q: q.where(
                ComentarioTareaConfiguration.amonet_tarea_sprint_id == query.amonet_tarea_sprint_id,
                ComentarioTareaConfiguration.activo == True,
            ),
            loader_options=ComentarioTareaLoaderOptions.get(),
            order_by=ComentarioTareaConfiguration.fecha_alta.asc(),
        )

        return [ComentarioTareaMapper.to_response(m) for m in items]
