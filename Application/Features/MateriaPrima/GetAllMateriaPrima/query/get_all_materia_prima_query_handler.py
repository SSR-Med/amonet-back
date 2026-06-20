from datetime import datetime, timedelta
from typing import Dict
from uuid import UUID

from sqlalchemy import func, select, true as sa_true
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos import (
    MateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.mappers import (
    MateriaPrimaLoaderOptions,
    MateriaPrimaMapper,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.query import (
    GetAllMateriaPrimaQuery,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.query_builders import (
    MateriaPrimaQueryBuilder,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
    InventarioMateriaPrimaContenedorConfiguration,
    MateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetAllMateriaPrimaQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MateriaPrimaConfiguration)
        self._session = session

    async def handle(
        self, query: GetAllMateriaPrimaQuery
    ) -> PaginatedResult[MateriaPrimaResponseDto]:
        items, page, total, page_size = await self._repository.get_all(
            page=query.page,
            page_size=query.page_size,
            where=MateriaPrimaQueryBuilder(query).build(),
            loader_options=MateriaPrimaLoaderOptions.get(),
        )

        mp_ids = [item.id_amonet_materia_prima for item in items]
        quantity_map = await self._get_quantities(mp_ids)

        return MateriaPrimaMapper.to_paginated_response(
            items, page, total, page_size, quantity_map
        )

    async def _get_quantities(self, mp_ids: list) -> Dict[UUID, float]:
        if not mp_ids:
            return {}

        one_year_ago = datetime.utcnow() - timedelta(days=365)
        stmt = (
            select(
                InventarioMateriaPrimaConfiguration.amonet_materia_prima_id,
                func.coalesce(
                    func.sum(InventarioMateriaPrimaContenedorConfiguration.cantidad_disponible), 0
                ).label("total"),
            )
            .outerjoin(
                InventarioMateriaPrimaContenedorConfiguration,
                InventarioMateriaPrimaContenedorConfiguration.amonet_inventario_materia_prima_id
                == InventarioMateriaPrimaConfiguration.id_amonet_inventario_materia_prima,
            )
            .where(
                InventarioMateriaPrimaConfiguration.amonet_materia_prima_id.in_(mp_ids),
                InventarioMateriaPrimaConfiguration.status == sa_true(),
                InventarioMateriaPrimaConfiguration.fecha_ingreso >= one_year_ago,
            )
            .group_by(
                InventarioMateriaPrimaConfiguration.amonet_materia_prima_id
            )
        )
        result = await self._session.execute(stmt)
        return {row[0]: float(row[1]) for row in result}
