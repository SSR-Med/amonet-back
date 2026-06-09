from uuid import UUID

from core.exceptions import NotFoundException
from core.interfaces import IRepository, IUnitOfWork
from infrastructure.dataaccess.configurations import MarcaConfiguration


class DeleteMarcaCommandHandler:

    def __init__(
        self,
        repository: IRepository[MarcaConfiguration],
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    async def handle(self, id: UUID) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == id)
        )
        if model is None:
            raise NotFoundException("Marca", str(id))

        await self._repository.delete(
            lambda q: q.where(MarcaConfiguration.id_amonet_marca == id)
        )
        await self._unit_of_work.commit()
