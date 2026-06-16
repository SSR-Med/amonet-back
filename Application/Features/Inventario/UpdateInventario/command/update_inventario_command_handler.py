from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Inventario.CreateInventario.validators import FileValidator
from Application.Features.Inventario.UpdateInventario.command import (
    UpdateInventarioCommand,
)
from Application.Features.Inventario.UpdateInventario.mappers import (
    UpdateInventarioMapper,
)
from core.constants import ADMIN
from core.dtos import AuditLogDto, CurrentUserDto, ObjectStorageUploadDto
from core.exceptions import NotFoundException, UnauthorizedException
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
    InventarioMateriaPrimaContenedorConfiguration,
)
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger, ObjectStorageService, get_settings


class UpdateInventarioCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._unit_of_work = UnitOfWork(session)
        self._storage = ObjectStorageService()

    async def handle(
        self, id: UUID, command: UpdateInventarioCommand, current_user: CurrentUserDto
    ) -> None:
        model = await self._get_model(id)
        self._check_permissions(current_user, model)

        UpdateInventarioMapper.apply(model, command)
        model.usuario_modifica = current_user.id
        model.fecha_modifica = datetime.now(timezone.utc)

        self._handle_file(command, model)
        await self._handle_contenedores(command, id)

        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

    async def _get_model(self, id: UUID) -> InventarioMateriaPrimaConfiguration:
        result = await self._session.execute(
            select(InventarioMateriaPrimaConfiguration).where(
                InventarioMateriaPrimaConfiguration.id_amonet_inventario_materia_prima == id
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise NotFoundException("Inventario", str(id))
        return model

    def _check_permissions(
        self, current_user: CurrentUserDto, model: InventarioMateriaPrimaConfiguration
    ) -> None:
        if current_user.rol != ADMIN and model.status is not None:
            raise UnauthorizedException("Only ADMIN can edit non-pending inventory")

    def _handle_file(
        self, command: UpdateInventarioCommand, model: InventarioMateriaPrimaConfiguration
    ) -> None:
        if command.archivo is None or command.nombre_archivo is None:
            return

        if model.ruta_evidencia:
            self._storage.delete(model.ruta_evidencia)

        FileValidator.validate_is_compressed(command.archivo)
        settings = get_settings()
        ruta = f"{settings.S3_EVIDENCIA_PREFIX}/{model.numero_ingreso}"

        self._storage.upload(ObjectStorageUploadDto(
            ruta=ruta,
            archivo=command.archivo,
            nombre_archivo=command.nombre_archivo,
        ))
        model.ruta_evidencia = f"{ruta}/{command.nombre_archivo}"

    async def _handle_contenedores(
        self, command: UpdateInventarioCommand, inventario_id: UUID
    ) -> None:
        if command.contenedores is None:
            return

        existing = await self._session.execute(
            select(InventarioMateriaPrimaContenedorConfiguration).where(
                InventarioMateriaPrimaContenedorConfiguration.amonet_inventario_materia_prima_id == inventario_id
            )
        )
        for old in existing.scalars().all():
            await self._session.delete(old)

        nuevos = UpdateInventarioMapper.build_contenedores(inventario_id, command.contenedores)
        for c in nuevos:
            self._session.add(c)
