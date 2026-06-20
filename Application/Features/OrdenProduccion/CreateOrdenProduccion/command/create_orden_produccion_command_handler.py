from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.command import (
    CreateOrdenProduccionCommand,
)
from Application.Features.OrdenProduccion.CreateOrdenProduccion.validators import (
    CreateOrdenProduccionValidator,
)


class CreateOrdenProduccionCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._validator = CreateOrdenProduccionValidator(session)

    async def handle(self, command: CreateOrdenProduccionCommand) -> None:
        await self._validator.validate(command)
