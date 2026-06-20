from typing import List

from Application.Features.OrdenProduccion.GetAllEstadosProduccion.dtos import (
    EstadoProduccionResponseDto,
)
from infrastructure.dataaccess.configurations import (
    CatalogoEstadoProduccionConfiguration,
)


class EstadoProduccionMapper:

    @staticmethod
    def to_response(
        model: CatalogoEstadoProduccionConfiguration,
    ) -> EstadoProduccionResponseDto:
        return EstadoProduccionResponseDto(
            id=model.id_cat_amonet_estado_produccion,
            nombre=model.nombre,
        )

    @staticmethod
    def to_list(
        items: List[CatalogoEstadoProduccionConfiguration],
    ) -> List[EstadoProduccionResponseDto]:
        return [EstadoProduccionMapper.to_response(item) for item in items]
