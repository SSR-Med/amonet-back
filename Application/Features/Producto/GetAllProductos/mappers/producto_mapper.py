from typing import List

from sqlalchemy.orm import selectinload

from Application.Features.Producto.GetAllProductos.dtos import (
    MarcaInfoDto,
    MateriaPrimaEnProductoResponseDto,
    ProductoResponseDto,
)
from infrastructure.dataaccess.configurations import (
    ProductoConfiguration,
    ProductoMateriaPrimaConfiguration,
)


class ProductoLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(ProductoConfiguration.marca),
            selectinload(ProductoConfiguration.materias_primas).selectinload(
                ProductoMateriaPrimaConfiguration.materia_prima
            ),
        ]


class ProductoMapper:

    @staticmethod
    def to_response(
        model: ProductoConfiguration,
    ) -> ProductoResponseDto:
        return ProductoResponseDto(
            id=model.id_amonet_producto,
            codigo=model.codigo,
            nombre=model.nombre,
            marca=MarcaInfoDto(
                id=model.marca.id_amonet_marca,
                nombre=model.marca.nombre,
            ),
            materias_primas=[
                MateriaPrimaEnProductoResponseDto(
                    id=pm.materia_prima.id_amonet_materia_prima,
                    nombre=pm.materia_prima.nombre,
                    formula=pm.formula,
                )
                for pm in model.materias_primas
            ],
        )

    @staticmethod
    def to_list_response(
        items: List[ProductoConfiguration],
    ) -> List[ProductoResponseDto]:
        return [ProductoMapper.to_response(item) for item in items]
