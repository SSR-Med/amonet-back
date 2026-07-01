from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.ColumnaKanbanBoard.GetAllColumnaKanban.query import (
    GetAllColumnaKanbanQuery,
)


class ColumnaKanbanQueryBuilder:

    def __init__(self, dto: GetAllColumnaKanbanQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(ColumnaKanbanConfiguration.activo == True)
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(ColumnaKanbanConfiguration.nombre)
                ).like(f"%{self._dto.nombre.strip().upper()}%"),
            )
            .and_if_not_none(
                self._dto.posicion,
                lambda: ColumnaKanbanConfiguration.posicion == self._dto.posicion,
            )
            .build()
        )
