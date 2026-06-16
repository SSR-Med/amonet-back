from typing import List
from uuid import UUID, uuid4

from Application.Features.Inventario.UpdateInventario.command import (
    UpdateInventarioCommand,
)
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
    InventarioMateriaPrimaContenedorConfiguration,
)


class UpdateInventarioMapper:

    SIMPLE_FIELDS = [
        "fecha_ingreso",
        "numero_ingreso",
        "amonet_materia_prima_id",
        "fecha_vencimiento",
        "status",
    ]

    @staticmethod
    def apply(model: InventarioMateriaPrimaConfiguration, command: UpdateInventarioCommand) -> None:
        data = command.model_dump(exclude_none=True)

        for field in UpdateInventarioMapper.SIMPLE_FIELDS:
            if field in data:
                setattr(model, field, data[field])

        if "proveedor" in data:
            model.proveedor = data["proveedor"].strip().upper()
        if "lote" in data:
            model.lote = data["lote"].strip().upper()
        if "observacion_rechazo" in data:
            model.observacion_rechazo = data["observacion_rechazo"].strip().upper()

    @staticmethod
    def build_contenedores(
        inventario_id: UUID, contenedores_data: list
    ) -> List[InventarioMateriaPrimaContenedorConfiguration]:
        models = []
        for c in contenedores_data:
            models.append(
                InventarioMateriaPrimaContenedorConfiguration(
                    id_amonet_inventario_materia_prima_contenedor=uuid4(),
                    contador_materia_prima=c.contador,
                    cantidad=c.cantidad,
                    cantidad_disponible=c.cantidad_disponible,
                    precio=c.precio,
                    amonet_inventario_materia_prima_id=inventario_id,
                )
            )
        return models
