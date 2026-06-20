from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.dtos import (
    MateriaPrimaContenedorDto,
    MateriaPrimaDto,
)
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
    InventarioMateriaPrimaContenedorConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class ContenedorValidator:

    def __init__(self, session: AsyncSession) -> None:
        self._contenedor_repository = Repository(
            session, InventarioMateriaPrimaContenedorConfiguration
        )
        self._inventario_repository = Repository(
            session, InventarioMateriaPrimaConfiguration
        )

    async def validate(self, materias_primas: List[MateriaPrimaDto]) -> None:
        for mp_dto in materias_primas:
            total_contenedor = sum(c.cantidad for c in mp_dto.contenedores)
            if total_contenedor != mp_dto.cantidad:
                raise ConflictException(
                    f"Sum of container quantities ({total_contenedor}) does not match "
                    f"materia prima quantity ({mp_dto.cantidad})"
                )

            for cont_dto in mp_dto.contenedores:
                await self._validate_contenedor(cont_dto, mp_dto)

    async def _validate_contenedor(
        self,
        cont_dto: MateriaPrimaContenedorDto,
        mp_dto: MateriaPrimaDto,
    ) -> None:
        contenedor = await self._contenedor_repository.first_or_default(
            lambda q: q.where(
                InventarioMateriaPrimaContenedorConfiguration.id_amonet_inventario_materia_prima_contenedor
                == cont_dto.amonet_inventario_materia_prima_contenedor_id
            )
        )
        if contenedor is None:
            raise NotFoundException(
                "InventarioMateriaPrimaContenedor",
                str(cont_dto.amonet_inventario_materia_prima_contenedor_id),
            )

        inventario = await self._inventario_repository.first_or_default(
            lambda q: q.where(
                InventarioMateriaPrimaConfiguration.id_amonet_inventario_materia_prima
                == contenedor.amonet_inventario_materia_prima_id
            )
        )
        if inventario is None:
            raise NotFoundException(
                "InventarioMateriaPrima",
                str(contenedor.amonet_inventario_materia_prima_id),
            )

        if inventario.status is not True:
            raise ConflictException(
                f"Inventory '{contenedor.amonet_inventario_materia_prima_id}' is not active"
            )

        if inventario.amonet_materia_prima_id != mp_dto.amonet_materia_prima_id:
            raise ConflictException(
                f"Container '{cont_dto.amonet_inventario_materia_prima_contenedor_id}' "
                f"does not belong to materia prima '{mp_dto.amonet_materia_prima_id}'"
            )

        if cont_dto.cantidad > contenedor.cantidad_disponible:
            raise ConflictException(
                f"Container '{cont_dto.amonet_inventario_materia_prima_contenedor_id}' "
                f"has insufficient available quantity: requested {cont_dto.cantidad}, "
                f"available {contenedor.cantidad_disponible}"
            )
