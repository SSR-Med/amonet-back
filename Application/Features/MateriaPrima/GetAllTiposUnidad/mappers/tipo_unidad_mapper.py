from typing import List

from Application.Features.MateriaPrima.GetAllTiposUnidad.dtos import (
    TipoUnidadResponseDto,
)
from infrastructure.dataaccess.configurations import (
    CatalogoTipoUnidadConfiguration,
)


class TipoUnidadMapper:

    @staticmethod
    def to_response(
        model: CatalogoTipoUnidadConfiguration,
    ) -> TipoUnidadResponseDto:
        return TipoUnidadResponseDto(
            id=model.id_cat_amonet_tipo_unidad,
            nombre=model.nombre,
            abreviacion=model.abreviacion,
        )

    @staticmethod
    def to_list(
        items: List[CatalogoTipoUnidadConfiguration],
    ) -> List[TipoUnidadResponseDto]:
        return [TipoUnidadMapper.to_response(item) for item in items]
