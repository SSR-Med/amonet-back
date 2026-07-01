from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.PrioridadKanban.GetAllPrioridadKanban.query import (
    GetAllPrioridadKanbanQuery,
)


class PrioridadKanbanQueryBuilder:

    def __init__(self, dto: GetAllPrioridadKanbanQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(PrioridadKanbanConfiguration.activo == True)
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(PrioridadKanbanConfiguration.nombre)
                ).like(f"%{self._dto.nombre.strip().upper()}%"),
            )
            .build()
        )
