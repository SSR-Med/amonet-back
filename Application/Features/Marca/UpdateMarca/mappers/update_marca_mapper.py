from Application.Features.Marca.UpdateMarca.dtos import (
    UpdateMarcaCommandDto,
)
from infrastructure.dataaccess.configurations import MarcaConfiguration


class UpdateMarcaMapper:

    @staticmethod
    def apply(
        model: MarcaConfiguration,
        dto: UpdateMarcaCommandDto,
    ) -> MarcaConfiguration:
        model.nombre = dto.nombre
        return model
