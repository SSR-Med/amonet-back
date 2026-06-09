from uuid import uuid4

from Application.Features.MateriaPrima.CreateMateriaPrima.command import (
    CreateMateriaPrimaCommand,
)
from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)


class CreateMateriaPrimaMapper:

    @staticmethod
    def to_model(
        dto: CreateMateriaPrimaCommand,
    ) -> MateriaPrimaConfiguration:
        return MateriaPrimaConfiguration(
            id_amonet_materia_prima=uuid4(),
            nombre=dto.nombre,
            id_cat_amonet_tipo_materia_prima=dto.id_cat_amonet_tipo_materia_prima,
            id_cat_amonet_tipo_unidad=dto.id_cat_amonet_tipo_unidad,
        )
