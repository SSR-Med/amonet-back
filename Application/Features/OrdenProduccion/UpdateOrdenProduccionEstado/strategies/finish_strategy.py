from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.command import (
    UpdateOrdenProduccionEstadoCommand,
)
from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.strategies.base_strategy import (
    BaseStrategy,
)
from infrastructure.dataaccess.configurations import OrdenProduccionConfiguration


class FinishStrategy(BaseStrategy):

    async def execute(
        self,
        order: OrdenProduccionConfiguration,
        command: UpdateOrdenProduccionEstadoCommand,
        session: AsyncSession,
    ) -> None:
        order.amonet_estado_produccion_id = command.amonet_estado_produccion_id
