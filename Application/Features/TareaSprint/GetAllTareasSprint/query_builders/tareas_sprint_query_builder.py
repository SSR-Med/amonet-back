from typing import Callable

from sqlalchemy import func, or_

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
            .and_if_not_empty(
                self._dto.titulo,
                lambda: TareaSprintConfiguration.titulo.ilike(f"%{self._dto.titulo}%"),
            )
            .and_if_not_none(
                self._dto.amonet_sprint_id,
                lambda: TareaSprintConfiguration.amonet_sprint_id == self._dto.amonet_sprint_id,
            )
            .and_if_not_none(
                self._dto.amonet_prioridad_kanban_id,
                lambda: TareaSprintConfiguration.amonet_prioridad_kanban_id == self._dto.amonet_prioridad_kanban_id,
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
            .and_if_not_none(
                self._dto.tags,
                lambda: self._build_tags_filter(),
            )
            .build()
        )

    def _build_tags_filter(self):
        tag_str_ids = [str(t) for t in self._dto.tags]
        conditions = [
            func.jsonb_array_elements_text(TareaSprintConfiguration.tags) == tag_id
            for tag_id in tag_str_ids
        ]
        return or_(*conditions) if conditions else None
