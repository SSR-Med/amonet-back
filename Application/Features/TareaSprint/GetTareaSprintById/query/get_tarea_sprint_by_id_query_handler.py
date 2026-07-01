from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TareaSprint.CreateTareaSprint.dtos import (
    TareaSprintResponseDto,
)
from Application.Features.TareaSprint.CreateTareaSprint.mappers import (
    TareaSprintLoaderOptions,
    TareaSprintMapper,
)
from Application.Features.TareaSprint.GetTareaSprintById.query import (
    GetTareaSprintByIdQuery,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import TareaSprintConfiguration
from infrastructure.dataaccess.repository import Repository


class GetTareaSprintByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TareaSprintConfiguration)
        self._session = session

    async def handle(self, query: GetTareaSprintByIdQuery) -> TareaSprintResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(TareaSprintConfiguration.id_amonet_tarea_sprint == query.id),
            loader_options=TareaSprintLoaderOptions.get(),
        )
        if model is None:
            raise NotFoundException("TareaSprint", str(query.id))

        tag_lookup = await TareaSprintMapper.build_tag_lookup(self._session, model.tags or [])
        return TareaSprintMapper.to_response(model, tag_lookup=tag_lookup)
