from typing import Callable

from sqlalchemy import func

from infrastructure.dataaccess.configurations import (
    MateriaPrimaConfiguration,
)
from infrastructure.query_builder import QueryBuilder
from infrastructure.query_builder.query_builder import escape_like

from Application.Features.MateriaPrima.GetAllMateriaPrima.query import (
    GetAllMateriaPrimaQuery,
)


class MateriaPrimaQueryBuilder:

    def __init__(self, dto: GetAllMateriaPrimaQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_filter(MateriaPrimaConfiguration.status == True)
            .and_if_not_empty(
                self._dto.nombre,
                lambda: func.upper(
                    func.trim(MateriaPrimaConfiguration.nombre)
                ).like(
                    escape_like(self._dto.nombre.strip().upper()),
                    escape="\\",
                ),
            )
            .and_if_not_none(
                self._dto.id_cat_amonet_tipo_materia_prima,
                lambda: MateriaPrimaConfiguration.id_cat_amonet_tipo_materia_prima
                == self._dto.id_cat_amonet_tipo_materia_prima,
            )
            .and_if_not_none(
                self._dto.id_cat_amonet_tipo_unidad,
                lambda: MateriaPrimaConfiguration.id_cat_amonet_tipo_unidad
                == self._dto.id_cat_amonet_tipo_unidad,
            )
            .build()
        )
