from typing import List

from Application.Features.Marca.GetAllMarcas.dtos import (
    MarcaResponseDto,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import MarcaConfiguration


class MarcaMapper:

    @staticmethod
    def to_response(
        model: MarcaConfiguration,
    ) -> MarcaResponseDto:
        return MarcaResponseDto(
            id=model.id_amonet_marca,
            nombre=model.nombre,
        )

    @staticmethod
    def to_paginated_response(
        items: List[MarcaConfiguration],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[MarcaResponseDto]:
        return PaginatedResult(
            items=[MarcaMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
