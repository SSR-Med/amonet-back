from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.Marca.GetAllMarcas.dtos import (
    GetAllMarcasQueryDto,
)


class MarcaQueryBuilder:

    def __init__(self, dto: GetAllMarcasQueryDto) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(MarcaConfiguration.nombre)
                ).like(
                    f"%{self._dto.nombre.strip().upper()}%"
                ),
            )
            .build()
        )
