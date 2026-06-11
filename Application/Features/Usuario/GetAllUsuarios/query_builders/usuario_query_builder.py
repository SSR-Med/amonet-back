from typing import Callable

from sqlalchemy import func, true as sa_true

from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.query_builder import QueryBuilder

from Application.Features.Usuario.GetAllUsuarios.query import (
    GetAllUsuariosQuery,
)


class UsuarioQueryBuilder:

    def __init__(self, dto: GetAllUsuariosQuery) -> None:
        self._dto = dto

    def build(self) -> Callable:
        return (
            QueryBuilder()
            .and_if_not_empty(
                self._dto.documento,
                lambda: func.upper(
                    func.trim(UsuarioConfiguration.documento)
                ).like(
                    f"%{self._dto.documento.strip().upper()}%"
                ),
            )
            .and_if_not_empty(
                self._dto.rol,
                lambda: func.upper(
                    func.trim(UsuarioConfiguration.rol)
                ).like(
                    f"%{self._dto.rol.strip().upper()}%"
                ),
            )
            .and_if_not_none(
                self._dto.activo,
                lambda: UsuarioConfiguration.activo == sa_true()
                if self._dto.activo
                else UsuarioConfiguration.activo == False,
            )
            .build()
        )
