from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Application.Features.Producto.CreateProducto.dtos import (
    CreateProductoCommand,
)
from Application.Features.Producto.CreateProducto.mappers import (
    CreateProductoMapper,
)
from Application.Features.Producto.GetAllProductos.dtos import (
    ProductoResponseDto,
)
from Application.Features.Producto.GetAllProductos.mappers import (
    ProductoMapper,
)
from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import (
    MarcaConfiguration,
    MateriaPrimaConfiguration,
    ProductoConfiguration,
    ProductoMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class CreateProductoCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = Repository(session, ProductoConfiguration)
        self._marca_repo = Repository(session, MarcaConfiguration)
        self._materia_repo = Repository(session, MateriaPrimaConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateProductoCommand
    ) -> ProductoResponseDto:
        command.codigo = command.codigo.strip().upper()
        command.nombre = command.nombre.strip().upper()

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.codigo == command.codigo
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Producto with codigo '{command.codigo}' already exists"
            )

        marca = await self._marca_repo.first_or_default(
            lambda q: q.where(
                MarcaConfiguration.id_amonet_marca == command.id_amonet_marca
            )
        )
        if marca is None:
            raise ConflictException("Marca not found")

        mp_ids = [mp.id_amonet_materia_prima for mp in command.materias_primas]
        if len(mp_ids) != len(set(mp_ids)):
            raise ConflictException("Duplicate materia prima in the list")

        for mp_id in mp_ids:
            mp = await self._materia_repo.first_or_default(
                lambda q: q.where(
                    MateriaPrimaConfiguration.id_amonet_materia_prima == mp_id
                )
            )
            if mp is None:
                raise ConflictException(
                    f"Materia prima '{mp_id}' not found"
                )

        producto = CreateProductoMapper.to_producto_model(command)
        await self._repository.create(producto)

        relaciones = CreateProductoMapper.to_materia_prima_models(
            producto.id_amonet_producto, command
        )
        for rel in relaciones:
            self._session.add(rel)

        await self._unit_of_work.commit()

        stmt = (
            select(ProductoConfiguration)
            .where(ProductoConfiguration.id_amonet_producto == producto.id_amonet_producto)
            .options(
                selectinload(ProductoConfiguration.marca),
                selectinload(ProductoConfiguration.materias_primas).selectinload(
                    ProductoMateriaPrimaConfiguration.materia_prima
                ),
            )
        )
        result = await self._session.execute(stmt)
        loaded = result.scalar_one()

        return ProductoMapper.to_response(loaded)
