from typing import Callable

from infrastructure.dataaccess.configurations import SprintConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.Sprint.GetAllSprints.query import (
    GetAllSprintsQuery,
)


class SprintQueryBuilder:

    def __init__(self, dto: GetAllSprintsQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(SprintConfiguration.activo == True)
            .and_if_not_none(
                self._dto.fecha_inicial,
                lambda: SprintConfiguration.fecha_inicio >= self._dto.fecha_inicial,
            )
            .and_if_not_none(
                self._dto.fecha_final,
                lambda: SprintConfiguration.fecha_inicio <= self._dto.fecha_final,
            )
            .and_if_not_none(
                self._dto.principal,
                lambda: SprintConfiguration.principal == self._dto.principal,
            )
            .and_if_not_none(
                self._dto.contador,
                lambda: SprintConfiguration.contador == self._dto.contador,
            )
            .build()
        )
