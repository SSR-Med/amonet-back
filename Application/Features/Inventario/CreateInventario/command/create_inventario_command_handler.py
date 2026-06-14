from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Inventario.CreateInventario.command import (
    CreateInventarioCommand,
)
from Application.Features.Inventario.CreateInventario.enrichers import (
    CreateInventarioEnricher,
    ObjectStorageEnricher,
)
from Application.Features.Inventario.CreateInventario.mappers import (
    CreateInventarioMapper,
)
from Application.Features.Inventario.CreateInventario.validators import (
    FileValidator,
    MateriaPrimaValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import BadRequestException
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateInventarioCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._enricher = CreateInventarioEnricher(session)
        self._materia_prima_validator = MateriaPrimaValidator(session)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateInventarioCommand, current_user: CurrentUserDto
    ) -> None:
        FileValidator.validate_is_compressed(command.archivo)

        mp_ids = [item.amonet_materia_prima_id for item in command.items]
        await self._materia_prima_validator.validate_exist(mp_ids)

        for item in command.items:
            item.proveedor = item.proveedor.strip().upper()
            item.lote = item.lote.strip().upper()
            for c in item.cantidades:
                if c < 0:
                    raise BadRequestException("Cantidades must be >= 0")

        enriched_items = await self._enricher.enrich(command.items, current_user)

        ruta_evidencia = ObjectStorageEnricher.enrich(
            archivo=command.archivo,
            nombre_archivo=command.nombre_archivo,
            numero_ingreso=enriched_items[0].numero_ingreso,
        )

        for enriched in enriched_items:
            inventario = CreateInventarioMapper.to_inventario_model(enriched, ruta_evidencia)
            self._session.add(inventario)
            await self._session.flush()

            contenedores = CreateInventarioMapper.to_contenedor_models(
                inventario.id_amonet_inventario_materia_prima,
                enriched,
            )
            for contenedor in contenedores:
                self._session.add(contenedor)

        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(exclude={"archivo"}),
        ))
