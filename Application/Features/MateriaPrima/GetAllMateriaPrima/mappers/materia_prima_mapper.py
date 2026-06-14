from typing import Dict, List
from uuid import UUID

from sqlalchemy.orm import selectinload

from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos import (
    MateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos.catalogo_info_dto import (
    CatalogoInfoDto,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)


class MateriaPrimaLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(MateriaPrimaConfiguration.tipo_materia_prima),
            selectinload(MateriaPrimaConfiguration.tipo_unidad),
        ]


class MateriaPrimaMapper:

    @staticmethod
    def to_response(
        model: MateriaPrimaConfiguration,
        cantidad_disponible: float = 0,
    ) -> MateriaPrimaResponseDto:
        return MateriaPrimaResponseDto(
            id=model.id_amonet_materia_prima,
            nombre=model.nombre,
            tipo_materia_prima=CatalogoInfoDto(
                id=model.tipo_materia_prima.id_cat_amonet_tipo_materia_prima,
                nombre=model.tipo_materia_prima.nombre,
            ),
            tipo_unidad=CatalogoInfoDto(
                id=model.tipo_unidad.id_cat_amonet_tipo_unidad,
                nombre=model.tipo_unidad.nombre,
                abreviacion=model.tipo_unidad.abreviacion,
            ),
            cantidad_disponible=cantidad_disponible,
        )

    @staticmethod
    def to_paginated_response(
        items: List[MateriaPrimaConfiguration],
        page: int,
        total: int,
        page_size: int,
        quantity_map: Dict[UUID, float] = None,
    ) -> PaginatedResult[MateriaPrimaResponseDto]:
        if quantity_map is None:
            quantity_map = {}
        return PaginatedResult(
            items=[
                MateriaPrimaMapper.to_response(
                    item, quantity_map.get(item.id_amonet_materia_prima, 0)
                )
                for item in items
            ],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
