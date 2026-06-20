from typing import List

from sqlalchemy.orm import selectinload

from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.dtos import (
    ContenedorResponseDto,
    EstadoProduccionInfoDto,
    MateriaPrimaResponseDto,
    OrdenProduccionResponseDto,
    ProductoInfoDto,
    UsuarioInfoDto,
    VariableGlobalResponseDto,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaContenedorConfiguration,
    InventarioMateriaPrimaConfiguration,
    OrdenProduccionConfiguration,
    OrdenProduccionMateriaPrimaConfiguration,
    OrdenProduccionMateriaPrimaContenedorConfiguration,
    OrdenProduccionVariableGlobalConfiguration,
    ProductoConfiguration,
)


class OrdenProduccionLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(OrdenProduccionConfiguration.producto).selectinload(
                ProductoConfiguration.marca
            ),
            selectinload(OrdenProduccionConfiguration.estado_produccion),
            selectinload(OrdenProduccionConfiguration.usuario_alta_rel),
            selectinload(OrdenProduccionConfiguration.usuario_modifica_rel),
            selectinload(OrdenProduccionConfiguration.variables_globales).selectinload(
                OrdenProduccionVariableGlobalConfiguration.variable_materia_prima
            ),
            selectinload(OrdenProduccionConfiguration.materias_primas).selectinload(
                OrdenProduccionMateriaPrimaConfiguration.materia_prima
            ),
            selectinload(OrdenProduccionConfiguration.materias_primas).selectinload(
                OrdenProduccionMateriaPrimaConfiguration.contenedores
            ).selectinload(
                OrdenProduccionMateriaPrimaContenedorConfiguration.inventario_contenedor
            ).selectinload(
                InventarioMateriaPrimaContenedorConfiguration.inventario
            ),
        ]


class OrdenProduccionMapper:

    @staticmethod
    def to_response(
        model: OrdenProduccionConfiguration,
    ) -> OrdenProduccionResponseDto:
        producto = model.producto
        marca = producto.marca if producto else None

        usuario_alta_rel = model.usuario_alta_rel
        usuario_modifica_rel = model.usuario_modifica_rel

        variables_globales = [
            VariableGlobalResponseDto(
                id=vg.id_amonet_orden_produccion_variable_global,
                nombre=vg.variable_materia_prima.nombre if vg.variable_materia_prima else "",
                cantidad=vg.cantidad,
            )
            for vg in (model.variables_globales or [])
        ]

        materias_primas = []
        for mp in (model.materias_primas or []):
            materia_prima = mp.materia_prima
            contenedores = []
            for c in (mp.contenedores or []):
                inv_contenedor = c.inventario_contenedor
                inventario = inv_contenedor.inventario if inv_contenedor else None
                contenedores.append(
                    ContenedorResponseDto(
                        id=c.id_amonet_orden_produccion_materia_prima_contenedor,
                        cantidad=c.cantidad,
                        coste=float(c.coste),
                        lote=inventario.lote if inventario else "",
                        proveedor=inventario.proveedor if inventario else "",
                    )
                )
            materias_primas.append(
                MateriaPrimaResponseDto(
                    id=mp.id_amonet_orden_produccion_materia_prima,
                    nombre=materia_prima.nombre if materia_prima else "",
                    contenedores=contenedores,
                )
            )

        return OrdenProduccionResponseDto(
            id=model.id_amonet_orden_produccion,
            descripcion=model.descripcion,
            observacion_creacion=model.observacion_creacion,
            fecha_alta=model.fecha_alta,
            fecha_modifica=model.fecha_modifica,
            coste=float(model.coste),
            producto=ProductoInfoDto(
                id=producto.id_amonet_producto if producto else "",
                codigo=producto.codigo if producto else "",
                nombre=producto.nombre if producto else "",
                marca_nombre=marca.nombre if marca else "",
            ),
            estado_produccion=EstadoProduccionInfoDto(
                id=model.amonet_estado_produccion_id,
                nombre=model.estado_produccion.nombre if model.estado_produccion else "",
            ),
            usuario_alta=UsuarioInfoDto(
                id=usuario_alta_rel.id_amonet_usuario,
                documento=usuario_alta_rel.documento,
                nombre=usuario_alta_rel.nombre,
            ) if usuario_alta_rel else UsuarioInfoDto(
                id=model.usuario_alta, documento="", nombre=""
            ),
            usuario_modifica=UsuarioInfoDto(
                id=usuario_modifica_rel.id_amonet_usuario,
                documento=usuario_modifica_rel.documento,
                nombre=usuario_modifica_rel.nombre,
            ) if usuario_modifica_rel else None,
            variables_globales=variables_globales,
            materias_primas=materias_primas,
        )

    @staticmethod
    def to_paginated_response(
        items: List[OrdenProduccionConfiguration],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[OrdenProduccionResponseDto]:
        return PaginatedResult(
            items=[OrdenProduccionMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
