from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.query_builder import QueryBuilder

from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    GetAllVariablesGlobalesQueryDto,
)


class VariablesGlobalesMateriaPrimaQueryBuilder:

    def __init__(self, dto: GetAllVariablesGlobalesQueryDto) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(VariablesGlobalesMateriaPrimaConfiguration.nombre)
                ).like(
                    f"%{self._dto.nombre.strip().upper()}%"
                ),
            )
            .build()
        )
