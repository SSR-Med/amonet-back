from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    GetAllVariablesGlobalesQueryDto,
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.query_builders import (
    VariablesGlobalesMateriaPrimaQueryBuilder,
)
from core.dtos import PaginatedResult
from core.interfaces import IRepository
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class GetAllVariablesGlobalesQueryHandler:

    def __init__(
        self, repository: IRepository[VariablesGlobalesMateriaPrimaConfiguration]
    ) -> None:
        self._repository = repository

    async def handle(
        self, dto: GetAllVariablesGlobalesQueryDto
    ) -> PaginatedResult[VariablesGlobalesMateriaPrimaResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=dto.page,
            page_size=dto.page_size,
            where=VariablesGlobalesMateriaPrimaQueryBuilder(dto).build(),
        )

        return VariablesGlobalesMateriaPrimaMapper.to_paginated_response(
            items, page, total, page_size
        )
