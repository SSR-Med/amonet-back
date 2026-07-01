from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import TagKanbanConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.TagKanban.GetAllTagsKanban.query import (
    GetAllTagsKanbanQuery,
)


class TagKanbanQueryBuilder:

    def __init__(self, dto: GetAllTagsKanbanQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(TagKanbanConfiguration.activo == True)
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(TagKanbanConfiguration.nombre)
                ).like(f"%{self._dto.nombre.strip().upper()}%"),
            )
            .build()
        )
