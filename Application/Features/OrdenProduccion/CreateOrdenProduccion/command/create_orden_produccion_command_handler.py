from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.command import (
    CreateOrdenProduccionCommand,
)
from Application.Features.OrdenProduccion.CreateOrdenProduccion.enrichers import (
    CosteEnricher,
    EstadoProduccionEnricher,
)
from Application.Features.OrdenProduccion.CreateOrdenProduccion.mappers import (
    CreateOrdenProduccionMapper,
)
from Application.Features.OrdenProduccion.CreateOrdenProduccion.validators import (
    CreateOrdenProduccionValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaContenedorConfiguration,
    OrdenProduccionConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateOrdenProduccionCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._validator = CreateOrdenProduccionValidator(session)
        self._estado_enricher = EstadoProduccionEnricher(session)
        self._coste_enricher = CosteEnricher(session)
        self._mapper = CreateOrdenProduccionMapper()
        self._repository = Repository(session, OrdenProduccionConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self, command: CreateOrdenProduccionCommand, current_user: CurrentUserDto
    ) -> None:
        try:
            await self._validator.validate(command)

            estado_id = await self._estado_enricher.enrich()
            costes_contenedor = await self._coste_enricher.enrich(
                command.materias_primas
            )

            model = self._mapper.to_model(
                command, current_user.id, estado_id, costes_contenedor
            )

            await self._repository.create(model)

            for mp in command.materias_primas:
                for cont_dto in mp.contenedores:
                    result = await self._session.execute(
                        update(InventarioMateriaPrimaContenedorConfiguration)
                        .where(
                            InventarioMateriaPrimaContenedorConfiguration.id_amonet_inventario_materia_prima_contenedor
                            == cont_dto.amonet_inventario_materia_prima_contenedor_id,
                            InventarioMateriaPrimaContenedorConfiguration.cantidad_disponible >= cont_dto.cantidad,
                        )
                        .values(
                            cantidad_disponible=InventarioMateriaPrimaContenedorConfiguration.cantidad_disponible - cont_dto.cantidad
                        )
                    )
                    if result.rowcount == 0:
                        raise ConflictException(
                            f"Insufficient stock in container {cont_dto.amonet_inventario_materia_prima_contenedor_id}: requested {cont_dto.cantidad}"
                        )

            await self._unit_of_work.commit()

            AuditLogger.log(AuditLogDto(
                usuario=current_user.documento,
                feature=type(self).__name__,
                datos=command.model_dump(),
            ))

        except Exception:
            await self._unit_of_work.rollback()
            raise
