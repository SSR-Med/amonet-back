from typing import List
from uuid import UUID

from Application.Features.Inventario.CreateInventario.dtos import EnrichedItem
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
    InventarioMateriaPrimaContenedorConfiguration,
)


class CreateInventarioMapper:

    @staticmethod
    def to_inventario_model(
        enriched: EnrichedItem, ruta_evidencia: str
    ) -> InventarioMateriaPrimaConfiguration:
        return InventarioMateriaPrimaConfiguration(
            fecha_ingreso=enriched.fecha_ingreso,
            numero_ingreso=enriched.numero_ingreso,
            amonet_materia_prima_id=enriched.dto.amonet_materia_prima_id,
            proveedor=enriched.dto.proveedor,
            lote=enriched.dto.lote,
            fecha_vencimiento=enriched.dto.fecha_vencimiento,
            usuario_alta=enriched.usuario_alta,
            status=enriched.status,
            ruta_evidencia=ruta_evidencia,
        )

    @staticmethod
    def to_contenedor_models(
        inventario_id: UUID, enriched: EnrichedItem
    ) -> List[InventarioMateriaPrimaContenedorConfiguration]:
        models = []
        for i, cantidad in enumerate(enriched.dto.cantidades, start=1):
            models.append(
                InventarioMateriaPrimaContenedorConfiguration(
                    contador_materia_prima=i,
                    cantidad=float(cantidad),
                    amonet_inventario_materia_prima_id=inventario_id,
                )
            )
        return models
