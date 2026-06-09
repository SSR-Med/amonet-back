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
    def to_paginated_response(
        items: List[VariablesGlobalesMateriaPrimaConfiguration],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[VariablesGlobalesMateriaPrimaResponseDto]:
        return PaginatedResult(
            items=[
                VariablesGlobalesMateriaPrimaResponseDto(
                    id=item.id_amonet_variable_materia_prima,
                    nombre=item.nombre,
                )
                for item in items
            ],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
