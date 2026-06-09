from Application.Features.MateriaPrima.UpdateMateriaPrima.command import (
    UpdateMateriaPrimaCommand,
)
from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)


class UpdateMateriaPrimaMapper:

    @staticmethod
    def apply(
        model: MateriaPrimaConfiguration,
        dto: UpdateMateriaPrimaCommand,
    ) -> MateriaPrimaConfiguration:
        model.nombre = dto.nombre
        model.id_cat_amonet_tipo_materia_prima = dto.id_cat_amonet_tipo_materia_prima
        model.id_cat_amonet_tipo_unidad = dto.id_cat_amonet_tipo_unidad
        return model
