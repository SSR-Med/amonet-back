import logging
import re
from datetime import date
from pathlib import Path

from core.constants import LOGS
from core.dtos import ObjectStorageUploadDto
from infrastructure.services.object_storage import ObjectStorageService

logger = logging.getLogger(__name__)

LOG_DIR = LOGS
S3_LOG_PREFIX = LOGS
LOG_FILENAME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.log$")


class LogUploader:

    @staticmethod
    def upload_old_logs() -> None:
        today = date.today().isoformat()
        storage = ObjectStorageService()

        for filepath in Path(LOG_DIR).glob("*.log"):
            if filepath.stem >= today:
                continue

            if not LOG_FILENAME_PATTERN.match(filepath.name):
                logger.warning("Skipping log file with unexpected name: %s", filepath.name)
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
                logger.info("Uploaded and removed log file: %s", filepath.name)
            except Exception as e:
                logger.error("Failed to upload log file %s: %s", filepath.name, e)
