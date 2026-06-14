from datetime import datetime, timezone
from typing import List
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Inventario.CreateInventario.dtos import (
    CreateInventarioItemDto,
    EnrichedItem,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
)


class CreateInventarioEnricher:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def enrich(
        self, items: List[CreateInventarioItemDto], current_user: CurrentUserDto
    ) -> List[EnrichedItem]:
        now = datetime.now(timezone.utc)
        year = now.year
        month = now.month
        last_digit_year = year % 10
        sequential = await self._get_next_sequential(year, month)

        enriched: List[EnrichedItem] = []
        for dto in items:
            numero_ingreso = f"{last_digit_year}{month}{sequential}"
            sequential += 1
            enriched.append(EnrichedItem(
                dto=dto,
                fecha_ingreso=now,
                numero_ingreso=numero_ingreso,
                usuario_alta=current_user.id,
            ))

        return enriched

    async def _get_next_sequential(self, year: int, month: int) -> int:
        year_prefix = str(year % 10)
        month_prefix = str(month)

        result = await self._session.execute(
            select(func.max(InventarioMateriaPrimaConfiguration.numero_ingreso)).where(
                InventarioMateriaPrimaConfiguration.numero_ingreso.like(
                    f"{year_prefix}{month_prefix}%"
                )
            )
        )
        max_numero = result.scalar_one_or_none()

        if max_numero is None:
            return 1

        prefix_len = len(year_prefix) + len(month_prefix)
        try:
            return int(max_numero[prefix_len:]) + 1
        except (ValueError, IndexError):
            return 1
