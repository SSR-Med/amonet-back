from typing import List, Optional
from uuid import UUID


class MarcaInfoDto:
    def __init__(self, id: UUID, nombre: str) -> None:
        self.id = id
        self.nombre = nombre


class MateriaPrimaEnProductoResponseDto:
    def __init__(
        self, id: UUID, nombre: str, formula: Optional[str] = None
    ) -> None:
        self.id = id
        self.nombre = nombre
        self.formula = formula


class ProductoResponseDto:
    def __init__(
        self,
        id: UUID,
        codigo: str,
        nombre: str,
        marca: MarcaInfoDto,
        materias_primas: List[MateriaPrimaEnProductoResponseDto],
    ) -> None:
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.materias_primas = materias_primas
