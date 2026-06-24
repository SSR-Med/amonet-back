from typing import Callable

from sqlalchemy import select

from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.query import (
    GetAllOrdenesProduccionQuery,
)
from infrastructure.dataaccess.configurations import (
    OrdenProduccionConfiguration,
    OrdenProduccionMateriaPrimaConfiguration,
)
from infrastructure.query_builder import QueryBuilder


class OrdenProduccionQueryBuilder:

    def __init__(self, dto: GetAllOrdenesProduccionQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        subquery = (
            select(OrdenProduccionMateriaPrimaConfiguration.amonet_orden_produccion_id)
            .where(
                OrdenProduccionMateriaPrimaConfiguration.amonet_materia_prima_id
                == self._dto.amonet_materia_prima_id
            )
        )

        return (
            QueryBuilder()
            .and_if_not_none(
                self._dto.fecha_min,
                lambda: OrdenProduccionConfiguration.fecha_alta
                >= self._dto.fecha_min,
            )
            .and_if_not_none(
                self._dto.fecha_max,
                lambda: OrdenProduccionConfiguration.fecha_alta
                <= f"{self._dto.fecha_max} 23:59:59",
            )
            .and_if_not_none(
                self._dto.amonet_producto_id,
                lambda: OrdenProduccionConfiguration.amonet_producto_id
                == self._dto.amonet_producto_id,
            )
            .and_if_not_none(
                self._dto.amonet_estado_produccion_id,
                lambda: OrdenProduccionConfiguration.amonet_estado_produccion_id
                == self._dto.amonet_estado_produccion_id,
            )
            .and_if_not_none(
                self._dto.amonet_materia_prima_id,
                lambda: OrdenProduccionConfiguration.id_amonet_orden_produccion.in_(
                    subquery
                ),
            )
            .build()
        )
