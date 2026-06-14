from typing import Callable

from sqlalchemy import func

from Application.Features.Inventario.GetAllInventario.query import (
    GetAllInventarioQuery,
)
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
)
from infrastructure.query_builder import QueryBuilder


class InventarioQueryBuilder:

    def __init__(self, dto: GetAllInventarioQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_if_not_none(
                self._dto.status,
                lambda: InventarioMateriaPrimaConfiguration.status == self._dto.status,
            )
            .and_if_not_empty(
                self._dto.lote,
                lambda: func.upper(
                    func.trim(InventarioMateriaPrimaConfiguration.lote)
                ).like(f"%{self._dto.lote.strip().upper()}%"),
            )
            .and_if_not_none(
                self._dto.amonet_materia_prima_id,
                lambda: InventarioMateriaPrimaConfiguration.amonet_materia_prima_id
                == self._dto.amonet_materia_prima_id,
            )
            .and_if_not_none(
                self._dto.fecha_inicio,
                lambda: InventarioMateriaPrimaConfiguration.fecha_ingreso
                >= self._dto.fecha_inicio,
            )
            .and_if_not_none(
                self._dto.fecha_fin,
                lambda: InventarioMateriaPrimaConfiguration.fecha_ingreso
                <= f"{self._dto.fecha_fin} 23:59:59",
            )
            .and_if_not_empty(
                self._dto.proveedor,
                lambda: func.upper(
                    func.trim(InventarioMateriaPrimaConfiguration.proveedor)
                ).like(f"%{self._dto.proveedor.strip().upper()}%"),
            )
            .and_if_not_none(
                self._dto.usuario_alta,
                lambda: InventarioMateriaPrimaConfiguration.usuario_alta
                == self._dto.usuario_alta,
            )
            .build()
        )
