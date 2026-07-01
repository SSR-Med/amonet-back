from typing import Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TareaSprint.CreateTareaSprint.dtos import (
    TareaSprintResponseDto,
)
from Application.Features.TareaSprint.CreateTareaSprint.mappers import (
    TareaSprintLoaderOptions,
    TareaSprintMapper,
)
from Application.Features.TareaSprint.GetAllTareasSprint.query import (
    GetAllTareasSprintQuery,
)
from Application.Features.TareaSprint.GetAllTareasSprint.query_builders import (
    TareasSprintQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import TareaSprintConfiguration
from infrastructure.dataaccess.repository import Repository


class GetAllTareasSprintQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, TareaSprintConfiguration)
        self._session = session

    async def _collect_tag_ids(self, items: List[TareaSprintConfiguration]) -> List[UUID]:
        ids: set = set()
        for item in items:
            if item.tags:
                for tag_id in item.tags:
                    ids.add(UUID(tag_id) if isinstance(tag_id, str) else tag_id)
        return list(ids)

    async def handle(
        self, query: GetAllTareasSprintQuery
    ) -> PaginatedResult[TareaSprintResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=TareasSprintQueryBuilder(query).build(),
            loader_options=TareaSprintLoaderOptions.get(),
            order_by=TareaSprintConfiguration.fecha_alta.desc(),
        )

        tag_ids = await self._collect_tag_ids(items)
        tag_lookup = await TareaSprintMapper.build_tag_lookup(self._session, tag_ids)

        return PaginatedResult(
            items=[TareaSprintMapper.to_response(item, tag_lookup=tag_lookup) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
