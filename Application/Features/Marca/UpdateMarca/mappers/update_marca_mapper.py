from Application.Features.Marca.UpdateMarca.command import (
    UpdateMarcaCommand,
)
from infrastructure.dataaccess.configurations import MarcaConfiguration


class UpdateMarcaMapper:

    @staticmethod
    def apply(
        model: MarcaConfiguration,
        dto: UpdateMarcaCommand,
    ) -> MarcaConfiguration:
        model.nombre = dto.nombre
        return model
