from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos import (
    MateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.mappers import (
    MateriaPrimaMapper,
)
from Application.Features.MateriaPrima.UpdateMateriaPrima.command import (
    UpdateMateriaPrimaCommand,
)
from Application.Features.MateriaPrima.UpdateMateriaPrima.mappers import (
    UpdateMateriaPrimaMapper,
)
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import (
    CatalogoTipoMateriaPrimaConfiguration,
    CatalogoTipoUnidadConfiguration,
    MateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class UpdateMateriaPrimaCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MateriaPrimaConfiguration)
        self._tipo_materia_repo = Repository(
            session, CatalogoTipoMateriaPrimaConfiguration
        )
        self._tipo_unidad_repo = Repository(
            session, CatalogoTipoUnidadConfiguration
        )
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, id: UUID, command: UpdateMateriaPrimaCommand
    ) -> MateriaPrimaResponseDto:
        command.nombre = command.nombre.strip().upper()

        model = await self._repository.first_or_default(
            lambda q: q.where(
                MateriaPrimaConfiguration.id_amonet_materia_prima == id
            )
        )
        if model is None:
            raise NotFoundException("MateriaPrima", str(id))

        existing = await self._repository.first_or_default(
            lambda q: q.where(
                MateriaPrimaConfiguration.nombre == command.nombre,
                MateriaPrimaConfiguration.id_amonet_materia_prima != id,
            )
        )
        if existing is not None:
            raise ConflictException(
                f"Materia prima '{command.nombre}' already exists"
            )

        tipo_exists = await self._tipo_materia_repo.first_or_default(
            lambda q: q.where(
                CatalogoTipoMateriaPrimaConfiguration.id_cat_amonet_tipo_materia_prima
                == command.id_cat_amonet_tipo_materia_prima
            )
        )
        if tipo_exists is None:
            raise ConflictException("Tipo materia prima not found")

        unidad_exists = await self._tipo_unidad_repo.first_or_default(
            lambda q: q.where(
                CatalogoTipoUnidadConfiguration.id_cat_amonet_tipo_unidad
                == command.id_cat_amonet_tipo_unidad
            )
        )
        if unidad_exists is None:
            raise ConflictException("Tipo unidad not found")

        model = UpdateMateriaPrimaMapper.apply(model, command)
        await self._repository.update(model)
        await self._unit_of_work.commit()

        return MateriaPrimaMapper.to_response(model)
