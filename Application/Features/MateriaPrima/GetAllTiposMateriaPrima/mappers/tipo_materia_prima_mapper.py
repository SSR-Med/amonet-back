from typing import List

from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.dtos import (
    TipoMateriaPrimaResponseDto,
)
from infrastructure.dataaccess.configurations import (
    CatalogoTipoMateriaPrimaConfiguration,
)


class TipoMateriaPrimaMapper:

    @staticmethod
    def to_response(
        model: CatalogoTipoMateriaPrimaConfiguration,
    ) -> TipoMateriaPrimaResponseDto:
        return TipoMateriaPrimaResponseDto(
            id=model.id_cat_amonet_tipo_materia_prima,
            nombre=model.nombre,
        )

    @staticmethod
    def to_list(
        items: List[CatalogoTipoMateriaPrimaConfiguration],
    ) -> List[TipoMateriaPrimaResponseDto]:
        return [TipoMateriaPrimaMapper.to_response(item) for item in items]
