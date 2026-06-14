from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Inventario.DownloadEvidencia.query import (
    DownloadEvidenciaQuery,
)
from core.dtos import ObjectStorageDownloadDto
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaConfiguration,
)
from infrastructure.services import ObjectStorageService


class DownloadEvidenciaQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._storage = ObjectStorageService()

    async def handle(self, query: DownloadEvidenciaQuery) -> dict:
        result = await self._session.execute(
            select(InventarioMateriaPrimaConfiguration).where(
                InventarioMateriaPrimaConfiguration.numero_ingreso
                == query.numero_ingreso
            )
        )
        inventario = result.scalar_one_or_none()

        if inventario is None:
            raise NotFoundException("Inventario", query.numero_ingreso)

        url = self._storage.get_download_url(
            ObjectStorageDownloadDto(ruta=inventario.ruta_evidencia)
        )

        return {"url": url}
