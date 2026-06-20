from typing import Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.dtos import (
    MateriaPrimaDto,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaContenedorConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class CosteEnricher:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(
            session, InventarioMateriaPrimaContenedorConfiguration
        )

    async def enrich(
        self, materias_primas: list[MateriaPrimaDto]
    ) -> Dict[UUID, float]:
        costes: Dict[UUID, float] = {}

        for mp_dto in materias_primas:
            for cont_dto in mp_dto.contenedores:
                contenedor_id = cont_dto.amonet_inventario_materia_prima_contenedor_id
                contenedor = await self._repository.first_or_default(
                    lambda q: q.where(
                        InventarioMateriaPrimaContenedorConfiguration.id_amonet_inventario_materia_prima_contenedor
                        == contenedor_id
                    )
                )
                if contenedor is None:
                    raise NotFoundException(
                        "InventarioMateriaPrimaContenedor", str(contenedor_id)
                    )

                if contenedor.cantidad == 0:
                    coste = 0.0
                else:
                    coste = (cont_dto.cantidad / float(contenedor.cantidad)) * float(
                        contenedor.precio
                    )

                costes[contenedor_id] = round(coste, 2)

        return costes
