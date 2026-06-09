from uuid import UUID

from sqlalchemy.orm import selectinload

from Application.Features.Producto.CreateProducto.dtos import (
    MateriaPrimaEnProductoDto,
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
from Application.Features.Producto.UpdateProducto.command import (
    UpdateProductoCommand,
)
from Application.Features.Producto.UpdateProducto.mappers import (
    UpdateProductoMapper,
)
from Application.Features.Producto.validators import FormulaValidator
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import (
    MarcaConfiguration,
    MateriaPrimaConfiguration,
    ProductoConfiguration,
    ProductoMateriaPrimaConfiguration,
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class UpdateProductoCommandHandler:

    def __init__(self, session) -> None:
        self._repository = Repository(session, ProductoConfiguration)
        self._marca_repo = Repository(session, MarcaConfiguration)
        self._materia_repo = Repository(session, MateriaPrimaConfiguration)
        self._relacion_repo = Repository(
            session, ProductoMateriaPrimaConfiguration
        )
        self._formula_validator = FormulaValidator(
            Repository(session, VariablesGlobalesMateriaPrimaConfiguration)
        )
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, id: UUID, command: UpdateProductoCommand
    ) -> ProductoResponseDto:
        command.codigo = command.codigo.strip().upper()
        command.nombre = command.nombre.strip().upper()

        for mp in command.materias_primas:
            if mp.formula:
                await self._formula_validator.validate(mp.formula)

        model = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.id_amonet_producto == id
            )
        )
        if model is None:
            raise NotFoundException("Producto", str(id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.codigo == command.codigo,
                ProductoConfiguration.id_amonet_producto != id,
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

        model = UpdateProductoMapper.apply(model, command)

        await self._relacion_repo.delete(
            lambda q: q.where(
                ProductoMateriaPrimaConfiguration.id_amonet_producto == id
            )
        )

        relaciones = CreateProductoMapper.to_materia_prima_models(id, command)
        for rel in relaciones:
            await self._relacion_repo.create(rel)

        await self._unit_of_work.commit()

        loaded = await self._repository.first_or_default(
            lambda q: q.where(
                ProductoConfiguration.id_amonet_producto == id
            ).options(
                selectinload(ProductoConfiguration.marca),
                selectinload(ProductoConfiguration.materias_primas).selectinload(
                    ProductoMateriaPrimaConfiguration.materia_prima
                ),
            )
        )

        return ProductoMapper.to_response(loaded)
