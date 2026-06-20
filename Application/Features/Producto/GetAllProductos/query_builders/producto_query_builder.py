from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import ProductoConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.Producto.GetAllProductos.query import (
    GetAllProductosQuery,
)


class ProductoQueryBuilder:

    def __init__(self, dto: GetAllProductosQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(ProductoConfiguration.status == True)
            .and_if_not_empty(
                self._dto.codigo,
                lambda: func.upper(
                    func.trim(ProductoConfiguration.codigo)
                ).like(f"%{self._dto.codigo.strip().upper()}%"),
            )
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(ProductoConfiguration.nombre)
                ).like(f"%{self._dto.nombre.strip().upper()}%"),
            )
            .and_if_not_none(
                self._dto.id_amonet_marca,
                lambda: ProductoConfiguration.id_amonet_marca
                == self._dto.id_amonet_marca,
            )
            .build()
        )
