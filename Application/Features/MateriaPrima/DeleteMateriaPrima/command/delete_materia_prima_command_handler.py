from Application.Features.MateriaPrima.DeleteMateriaPrima.dtos import (
    DeleteMateriaPrimaCommand,
)
from core.exceptions import NotFoundException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)


class DeleteMateriaPrimaCommandHandler:

    def __init__(
        self,
        repository: IRepository[MateriaPrimaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(self, command: DeleteMateriaPrimaCommand) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                MateriaPrimaConfiguration.id_amonet_materia_prima == command.id
            )
        )
        if model is None:
            raise NotFoundException("MateriaPrima", str(command.id))

        await self._repository.delete(
            lambda q: q.where(
                MateriaPrimaConfiguration.id_amonet_materia_prima == command.id
            )
        )
        await self._unit_of_work.commit()
