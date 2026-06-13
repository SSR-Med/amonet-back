from datetime import date
from pathlib import Path

from core.constants import LOGS
from core.dtos import ObjectStorageUploadDto
from infrastructure.services.object_storage import ObjectStorageService

LOG_DIR = LOGS
S3_LOG_PREFIX = LOGS


class LogUploader:

    @staticmethod
    def upload_old_logs() -> None:
        today = date.today().isoformat()
        storage = ObjectStorageService()

        for filepath in Path(LOG_DIR).glob("*.log"):
            if filepath.stem >= today:
                continue

            try:
                fecha = filepath.stem
                year, month, _ = fecha.split("-")
                ruta = f"{S3_LOG_PREFIX}/{year}/{month}"

                with open(filepath, "rb") as f:
                    content = f.read()

                dto = ObjectStorageUploadDto(
                    ruta=ruta,
                    archivo=content,
                    nombre_archivo=filepath.name,
                )
                storage.upload(dto)
                filepath.unlink()
            except Exception:
                pass
