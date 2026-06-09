from uuid import uuid4

from Application.Features.MateriaPrima.CreateVariablesGlobales.command import (
    CreateVariablesGlobalesCommand,
)
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class CreateVariablesGlobalesMapper:

    @staticmethod
    def to_model(
        dto: CreateVariablesGlobalesCommand,
    ) -> VariablesGlobalesMateriaPrimaConfiguration:
        return VariablesGlobalesMateriaPrimaConfiguration(
            id_amonet_variable_materia_prima=uuid4(),
            nombre=dto.nombre,
        )
