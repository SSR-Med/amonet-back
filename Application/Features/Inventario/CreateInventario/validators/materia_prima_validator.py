from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import BadRequestException
from infrastructure.dataaccess.configurations import MateriaPrimaConfiguration


class MateriaPrimaValidator:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def validate_exist(self, ids: List[UUID]) -> None:
        for mp_id in ids:
            result = await self._session.execute(
                select(MateriaPrimaConfiguration).where(
                    MateriaPrimaConfiguration.id_amonet_materia_prima == mp_id
                )
            )
            if result.scalar_one_or_none() is None:
                raise BadRequestException(
                    f"Materia prima '{mp_id}' does not exist"
                )
