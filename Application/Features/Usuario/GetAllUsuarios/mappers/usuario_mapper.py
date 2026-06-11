from typing import List

from Application.Features.Usuario.GetAllUsuarios.dtos import (
    UsuarioResponseDto,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import UsuarioConfiguration


class UsuarioMapper:

    @staticmethod
    def to_response(
        model: UsuarioConfiguration,
    ) -> UsuarioResponseDto:
        return UsuarioResponseDto(
            id=model.id_amonet_usuario,
            documento=model.documento,
            nombre=model.nombre,
            rol=model.rol,
        )

    @staticmethod
    def to_paginated_response(
        items: List[UsuarioConfiguration],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[UsuarioResponseDto]:
        return PaginatedResult(
            items=[UsuarioMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
