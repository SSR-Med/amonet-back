from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.command import (
    UpdateOrdenProduccionEstadoCommand,
)
from infrastructure.dataaccess.configurations import OrdenProduccionConfiguration


class BaseStrategy(ABC):

    @abstractmethod
    async def execute(
        self,
        order: OrdenProduccionConfiguration,
        command: UpdateOrdenProduccionEstadoCommand,
        session: AsyncSession,
    ) -> None:
        pass
