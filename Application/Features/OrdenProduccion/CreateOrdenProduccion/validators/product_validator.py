from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import ProductoConfiguration
from infrastructure.dataaccess.repository import Repository


class ProductValidator:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ProductoConfiguration)

    async def validate(self, amonet_producto_id: UUID) -> None:
        product = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.id_amonet_producto == amonet_producto_id
            )
        )
        if product is None:
            raise NotFoundException("Producto", str(amonet_producto_id))
