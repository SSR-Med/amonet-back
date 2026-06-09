from Application.Features.MateriaPrima.UpdateVariablesGlobales.dtos import (
    UpdateVariablesGlobalesCommandDto,
)
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class UpdateVariablesGlobalesMapper:

    @staticmethod
    def apply(
        model: VariablesGlobalesMateriaPrimaConfiguration,
        dto: UpdateVariablesGlobalesCommandDto,
    ) -> VariablesGlobalesMateriaPrimaConfiguration:
        model.nombre = dto.nombre
        return model
