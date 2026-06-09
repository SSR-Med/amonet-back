from Application.Features.MateriaPrima.DeleteVariablesGlobales.dtos import (
    DeleteVariablesGlobalesCommand,
)
from core.exceptions import NotFoundException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class DeleteVariablesGlobalesCommandHandler:

    def __init__(
        self,
        repository: IRepository[VariablesGlobalesMateriaPrimaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(self, command: DeleteVariablesGlobalesCommand) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                == command.id
            )
        )
        if model is None:
            raise NotFoundException("VariablesGlobalesMateriaPrima", str(command.id))

        await self._repository.delete(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                == command.id
            )
        )
        await self._unit_of_work.commit()
