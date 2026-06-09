from uuid import uuid4

from Application.Features.Marca.CreateMarca.command import (
    CreateMarcaCommand,
)
from infrastructure.dataaccess.configurations import MarcaConfiguration


class CreateMarcaMapper:

    @staticmethod
    def to_model(
        dto: CreateMarcaCommand,
    ) -> MarcaConfiguration:
        return MarcaConfiguration(
            id_amonet_marca=uuid4(),
            nombre=dto.nombre,
        )
