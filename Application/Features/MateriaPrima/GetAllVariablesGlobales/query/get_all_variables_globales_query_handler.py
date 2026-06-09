from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.query import (
    GetAllVariablesGlobalesQuery,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.query_builders import (
    VariablesGlobalesMateriaPrimaQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllVariablesGlobalesQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, VariablesGlobalesMateriaPrimaConfiguration
        )

    async def handle(
        self, query: GetAllVariablesGlobalesQuery
    ) -> PaginatedResult[VariablesGlobalesMateriaPrimaResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=VariablesGlobalesMateriaPrimaQueryBuilder(query).build(),
        )

        return VariablesGlobalesMateriaPrimaMapper.to_paginated_response(
            items, page, total, page_size
        )
