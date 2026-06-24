from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.command import (
    UpdateOrdenProduccionEstadoCommand,
)
from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.strategies import (
    BaseStrategy,
    CancelStrategy,
    FinishStrategy,
)
from core.constants import (
    ADMIN,
    ESTADO_ORDEN_PRODUCCION_CANCELLED,
    ESTADO_ORDEN_PRODUCCION_FINISHED,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import (
    CatalogoEstadoProduccionConfiguration,
    OrdenProduccionConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class UpdateOrdenProduccionEstadoCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = Repository(session, OrdenProduccionConfiguration)
        self._unit_of_work = UnitOfWork(session)

    async def handle(
        self,
        orden_id: UUID,
        command: UpdateOrdenProduccionEstadoCommand,
        current_user: CurrentUserDto,
    ) -> None:
        try:
            order = await self._repository.first_or_default(
                lambda q: q.where(
                    OrdenProduccionConfiguration.id_amonet_orden_produccion
                    == orden_id
                )
            )
            if order is None:
                raise NotFoundException("OrdenProduccion", str(orden_id))

            current_estado = await self._session.get(
                CatalogoEstadoProduccionConfiguration,
                order.amonet_estado_produccion_id,
            )
            current_estado_nombre = (
                current_estado.nombre if current_estado else ""
            )

            target_estado = await self._session.get(
                CatalogoEstadoProduccionConfiguration,
                command.amonet_estado_produccion_id,
            )
            if target_estado is None:
                raise NotFoundException(
                    "CatalogoEstadoProduccion", str(command.amonet_estado_produccion_id)
                )

            if current_user.rol != ADMIN:
                if current_estado_nombre in (
                    ESTADO_ORDEN_PRODUCCION_FINISHED,
                    ESTADO_ORDEN_PRODUCCION_CANCELLED,
                ):
                    raise ConflictException(
                        f"Cannot update order in status '{current_estado_nombre}'"
                    )

            if target_estado.nombre == ESTADO_ORDEN_PRODUCCION_CANCELLED:
                strategy: BaseStrategy = CancelStrategy()
            elif target_estado.nombre == ESTADO_ORDEN_PRODUCCION_FINISHED:
                strategy = FinishStrategy()
            else:
                raise ConflictException(
                    f"Status '{target_estado.nombre}' is not supported for update"
                )

            await strategy.execute(order, command, self._session)

            await self._unit_of_work.commit()

            AuditLogger.log(AuditLogDto(
                usuario=current_user.documento,
                feature=type(self).__name__,
                datos=command.model_dump(),
            ))

        except Exception:
            await self._unit_of_work.rollback()
            raise
