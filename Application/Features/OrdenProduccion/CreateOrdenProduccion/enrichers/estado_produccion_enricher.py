from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import ESTADO_ORDEN_PRODUCCION_ORDENADO
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    CatalogoEstadoProduccionConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class EstadoProduccionEnricher:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, CatalogoEstadoProduccionConfiguration)

    async def enrich(self) -> UUID:
        estado = await self._repository.first_or_default(
            lambda q: q.where(
                CatalogoEstadoProduccionConfiguration.nombre
                == ESTADO_ORDEN_PRODUCCION_ORDENADO
            )
        )
        if estado is None:
            raise NotFoundException(
                "CatalogoEstadoProduccion", ESTADO_ORDEN_PRODUCCION_ORDENADO
            )
        return estado.id_cat_amonet_estado_produccion
