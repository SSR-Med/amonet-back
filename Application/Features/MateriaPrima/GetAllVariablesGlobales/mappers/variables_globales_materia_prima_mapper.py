from typing import List

from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class VariablesGlobalesMateriaPrimaMapper:

    @staticmethod
    def to_response(
        model: VariablesGlobalesMateriaPrimaConfiguration,
    ) -> VariablesGlobalesMateriaPrimaResponseDto:
        return VariablesGlobalesMateriaPrimaResponseDto(
            id=model.id_amonet_variable_materia_prima,
            nombre=model.nombre,
        )

    @staticmethod
    def to_paginated_response(
        items: List[VariablesGlobalesMateriaPrimaConfiguration],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[VariablesGlobalesMateriaPrimaResponseDto]:
        return PaginatedResult(
            items=[VariablesGlobalesMateriaPrimaMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
