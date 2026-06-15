from typing import List

from sqlalchemy.orm import selectinload

from Application.Features.Inventario.GetAllInventario.dtos import (
    ContenedorDto,
    InventarioResponseDto,
    UsuarioInfoDto,
)
from core.dtos import PaginatedResult
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
    MateriaPrimaConfiguration,
)


class InventarioLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(InventarioMateriaPrimaConfiguration.materia_prima).selectinload(
                MateriaPrimaConfiguration.tipo_unidad
            ),
            selectinload(InventarioMateriaPrimaConfiguration.usuario_alta_rel),
            selectinload(InventarioMateriaPrimaConfiguration.contenedores),
        ]


class InventarioMapper:

    @staticmethod
    def to_response(
        model: InventarioMateriaPrimaConfiguration,
    ) -> InventarioResponseDto:
        materia_prima = model.materia_prima
        usuario = model.usuario_alta_rel

        cantidad_total = sum(
            float(c.cantidad) for c in (model.contenedores or [])
        )
        numero_contenedores = len(model.contenedores or [])

        contenedores = [
            ContenedorDto(
                contador=c.contador_materia_prima,
                cantidad=float(c.cantidad),
                precio=c.precio,
                precio_unidad=round(c.precio / float(c.cantidad), 2) if c.cantidad > 0 else 0,
            )
            for c in (model.contenedores or [])
        ]

        unidad = materia_prima.tipo_unidad if materia_prima and materia_prima.tipo_unidad else None

        return InventarioResponseDto(
            id=model.id_amonet_inventario_materia_prima,
            fecha_ingreso=model.fecha_ingreso,
            numero_ingreso=model.numero_ingreso,
            materia_prima_nombre=materia_prima.nombre if materia_prima else "",
            unidad_abreviacion=unidad.abreviacion if unidad else "",
            proveedor=model.proveedor,
            lote=model.lote,
            fecha_vencimiento=model.fecha_vencimiento,
            usuario_alta=UsuarioInfoDto(
                id=usuario.id_amonet_usuario,
                documento=usuario.documento,
                nombre=usuario.nombre,
            ) if usuario else None,
            status=model.status,
            ruta_evidencia=model.ruta_evidencia,
            cantidad_total=cantidad_total,
            numero_contenedores=numero_contenedores,
            contenedores=contenedores,
        )

    @staticmethod
    def to_paginated_response(
        items: List[InventarioMateriaPrimaConfiguration],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[InventarioResponseDto]:
        return PaginatedResult(
            items=[InventarioMapper.to_response(item) for item in items],
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
