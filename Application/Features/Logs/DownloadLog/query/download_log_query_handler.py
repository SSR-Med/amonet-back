from pathlib import Path
from typing import Optional

from Application.Features.Logs.DownloadLog.query import DownloadLogQuery
from core.constants import LOGS
from core.dtos import ObjectStorageDownloadDto, ObjectStorageListDto
from infrastructure.services import ObjectStorageService


class DownloadLogResult:
    def __init__(self, origen: str, nombre: str, presigned_url: Optional[str] = None, local_path: Optional[Path] = None) -> None:
        self.origen = origen
        self.nombre = nombre
        self.presigned_url = presigned_url
        self.local_path = local_path


class DownloadLogQueryHandler:

    def __init__(self) -> None:
        self._storage = ObjectStorageService()

    async def handle(self, query: DownloadLogQuery) -> Optional[DownloadLogResult]:
        filename = query.nombre
        fecha = filename.replace(".log", "")

        s3_items = self._storage.list(ObjectStorageListDto(ruta=LOGS), recursive=True)
        for item in s3_items:
            if not item.es_directorio and item.nombre.endswith(filename):
                s3_key = f"{LOGS}/{item.nombre}"
                url = self._storage.get_download_url(ObjectStorageDownloadDto(ruta=s3_key))
                return DownloadLogResult(origen="s3", nombre=filename, presigned_url=url)

        local_file = Path(LOGS) / filename
        if local_file.exists():
            return DownloadLogResult(origen="local", nombre=filename, local_path=local_file)

        return None
