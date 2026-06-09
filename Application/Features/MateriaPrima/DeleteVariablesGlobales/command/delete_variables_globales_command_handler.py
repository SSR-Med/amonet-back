from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.DeleteVariablesGlobales.command import (
    DeleteVariablesGlobalesCommand,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class DeleteVariablesGlobalesCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, VariablesGlobalesMateriaPrimaConfiguration
        )
        self._unit_of_work = UnitOfWork(session)

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
