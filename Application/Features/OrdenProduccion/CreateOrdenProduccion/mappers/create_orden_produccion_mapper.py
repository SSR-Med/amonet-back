from typing import Dict
from uuid import UUID, uuid4

from Application.Features.OrdenProduccion.CreateOrdenProduccion.command import (
    CreateOrdenProduccionCommand,
)
from infrastructure.dataaccess.configurations import (
    OrdenProduccionConfiguration,
    OrdenProduccionMateriaPrimaConfiguration,
    OrdenProduccionMateriaPrimaContenedorConfiguration,
    OrdenProduccionVariableGlobalConfiguration,
)


class CreateOrdenProduccionMapper:

    @staticmethod
    def to_model(
        command: CreateOrdenProduccionCommand,
        usuario_alta: UUID,
        estado_produccion_id: UUID,
        costes_contenedor: Dict[UUID, float],
    ) -> OrdenProduccionConfiguration:
        orden_id = uuid4()

        variables_globales = [
            OrdenProduccionVariableGlobalConfiguration(
                id_amonet_orden_produccion_variable_global=uuid4(),
                amonet_orden_produccion_id=orden_id,
                amonet_variable_materia_prima_id=vg.amonet_variable_materia_prima_id,
                cantidad=vg.cantidad,
            )
            for vg in command.variables_globales
        ]

        total_coste = 0.0
        materias_primas = []

        for mp_dto in command.materias_primas:
            mp_id = uuid4()

            contenedores = []
            for cont_dto in mp_dto.contenedores:
                coste = costes_contenedor.get(
                    cont_dto.amonet_inventario_materia_prima_contenedor_id, 0.0
                )
                total_coste += coste
                contenedores.append(
                    OrdenProduccionMateriaPrimaContenedorConfiguration(
                        id_amonet_orden_produccion_materia_prima_contenedor=uuid4(),
                        amonet_inventario_materia_prima_contenedor_id=cont_dto.amonet_inventario_materia_prima_contenedor_id,
                        amonet_orden_produccion_materia_prima_id=mp_id,
                        cantidad=cont_dto.cantidad,
                        coste=coste,
                    )
                )

            materias_primas.append(
                OrdenProduccionMateriaPrimaConfiguration(
                    id_amonet_orden_produccion_materia_prima=mp_id,
                    amonet_materia_prima_id=mp_dto.amonet_materia_prima_id,
                    amonet_orden_produccion_id=orden_id,
                    contenedores=contenedores,
                )
            )

        return OrdenProduccionConfiguration(
            id_amonet_orden_produccion=orden_id,
            descripcion=command.descripcion,
            observacion_creacion=command.observaciones,
            amonet_producto_id=command.amonet_producto_id,
            usuario_alta=usuario_alta,
            amonet_estado_produccion_id=estado_produccion_id,
            coste=round(total_coste, 2),
            variables_globales=variables_globales,
            materias_primas=materias_primas,
        )
