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
from core.dtos import CurrentUserDto
from infrastructure.dataaccess.configurations import OrdenProduccionConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork


class CreateOrdenProduccionCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
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
            await self._unit_of_work.commit()

        except Exception:
            await self._unit_of_work.rollback()
            raise
