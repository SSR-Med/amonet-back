from Application.Features.Marca.GetAllMarcas.dtos import (
    GetAllMarcasQueryDto,
    MarcaResponseDto,
)
from Application.Features.Marca.GetAllMarcas.mappers import (
    MarcaMapper,
)
from Application.Features.Marca.GetAllMarcas.query_builders import (
    MarcaQueryBuilder,
)
from core.dtos import PaginatedResult
from core.interfaces import IRepository
from infrastructure.dataaccess.configurations import MarcaConfiguration


class GetAllMarcasQueryHandler:

    def __init__(
        self, repository: IRepository[MarcaConfiguration]
    ) -> None:
        self._repository = repository

    async def handle(
        self, dto: GetAllMarcasQueryDto
    ) -> PaginatedResult[MarcaResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=dto.page,
            page_size=dto.page_size,
            where=MarcaQueryBuilder(dto).build(),
        )

        return MarcaMapper.to_paginated_response(
            items, page, total, page_size
        )
