from Application.Features.Producto.UpdateProducto.command import (
    UpdateProductoCommand,
)
from infrastructure.dataaccess.configurations import (
    ProductoConfiguration,
)


class UpdateProductoMapper:

    @staticmethod
    def apply(
        model: ProductoConfiguration,
        command: UpdateProductoCommand,
    ) -> ProductoConfiguration:
        model.codigo = command.codigo
        model.nombre = command.nombre
        model.id_amonet_marca = command.id_amonet_marca
        return model
