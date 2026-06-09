from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Producto.DeleteProducto.command import (
    DeleteProductoCommand,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    ProductoConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class DeleteProductoCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ProductoConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(self, command: DeleteProductoCommand) -> None:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.id_amonet_producto == command.id
            )
        )
        if model is None:
            raise NotFoundException("Producto", str(command.id))

        await self._repository.delete(
            lambda q: q.where(
                ProductoConfiguration.id_amonet_producto == command.id
            )
        )
        await self._unit_of_work.commit()
