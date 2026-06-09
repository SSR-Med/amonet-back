from Application.Features.MateriaPrima.UpdateVariablesGlobales.command import (
    UpdateVariablesGlobalesCommand,
)
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class UpdateVariablesGlobalesMapper:

    @staticmethod
    def apply(
        model: VariablesGlobalesMateriaPrimaConfiguration,
        dto: UpdateVariablesGlobalesCommand,
    ) -> VariablesGlobalesMateriaPrimaConfiguration:
        model.nombre = dto.nombre
        return model
