from uuid import UUID

from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos.catalogo_info_dto import (
    CatalogoInfoDto,
)


class MateriaPrimaResponseDto:
    def __init__(
        self,
        id: UUID,
        nombre: str,
        tipo_materia_prima: CatalogoInfoDto,
        tipo_unidad: CatalogoInfoDto,
        cantidad_disponible: float = 0,
    ) -> None:
        self.id = id
        self.nombre = nombre
        self.tipo_materia_prima = tipo_materia_prima
        self.tipo_unidad = tipo_unidad
        self.cantidad_disponible = cantidad_disponible
