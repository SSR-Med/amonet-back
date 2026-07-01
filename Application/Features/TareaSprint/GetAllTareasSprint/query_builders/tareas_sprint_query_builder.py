from typing import Callable

from infrastructure.dataaccess.configurations import TareaSprintConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.TareaSprint.GetAllTareasSprint.query import (
    GetAllTareasSprintQuery,
)


class TareasSprintQueryBuilder:

    def __init__(self, dto: GetAllTareasSprintQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(TareaSprintConfiguration.activo == True)
            .and_if_not_none(
                self._dto.amonet_sprint_id,
                lambda: TareaSprintConfiguration.amonet_sprint_id == self._dto.amonet_sprint_id,
            )
            .and_if_not_none(
                self._dto.fecha_min,
                lambda: TareaSprintConfiguration.fecha_alta >= self._dto.fecha_min,
            )
            .and_if_not_none(
                self._dto.fecha_max,
                lambda: TareaSprintConfiguration.fecha_alta <= self._dto.fecha_max,
            )
            .and_if_not_none(
                self._dto.usuario_alta,
                lambda: TareaSprintConfiguration.usuario_alta == self._dto.usuario_alta,
            )
            .build()
        )
