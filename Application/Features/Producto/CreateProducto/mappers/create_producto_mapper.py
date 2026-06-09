from uuid import uuid4

from Application.Features.Producto.CreateProducto.command import (
    CreateProductoCommand,
)
from infrastructure.dataaccess.configurations import (
    ProductoConfiguration,
    ProductoMateriaPrimaConfiguration,
)


class CreateProductoMapper:

    @staticmethod
    def to_producto_model(
        command: CreateProductoCommand,
    ) -> ProductoConfiguration:
        return ProductoConfiguration(
            id_amonet_producto=uuid4(),
            codigo=command.codigo,
            nombre=command.nombre,
            id_amonet_marca=command.id_amonet_marca,
        )

    @staticmethod
    def to_materia_prima_models(
        producto_id, command: CreateProductoCommand
    ) -> list[ProductoMateriaPrimaConfiguration]:
        return [
            ProductoMateriaPrimaConfiguration(
                id_amonet_producto_materia_prima=uuid4(),
                id_amonet_producto=producto_id,
                id_amonet_materia_prima=mp.id_amonet_materia_prima,
                formula=mp.formula,
            )
            for mp in command.materias_primas
        ]
