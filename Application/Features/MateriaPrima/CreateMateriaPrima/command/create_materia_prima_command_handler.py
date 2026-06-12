from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.CreateMateriaPrima.command import (
    CreateMateriaPrimaCommand,
)
from Application.Features.MateriaPrima.CreateMateriaPrima.mappers import (
    CreateMateriaPrimaMapper,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.dtos import (
    MateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.mappers import (
    MateriaPrimaMapper,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import (
    CatalogoTipoMateriaPrimaConfiguration,
    CatalogoTipoUnidadConfiguration,
    MateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateMateriaPrimaCommandHandler:

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
        self, command: CreateMateriaPrimaCommand, current_user: CurrentUserDto
    ) -> MateriaPrimaResponseDto:
        command.nombre = command.nombre.strip().upper()

        existing = await self._repository.first_or_default(
            lambda q: q.where(MateriaPrimaConfiguration.nombre == command.nombre)
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

        model = CreateMateriaPrimaMapper.to_model(command)
        await self._repository.create(model)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return MateriaPrimaMapper.to_response(model)
