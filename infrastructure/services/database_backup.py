import re
import subprocess
import tempfile
from datetime import datetime, timedelta

from core.dtos import ObjectStorageListDto, ObjectStorageUploadDto
from infrastructure.services.object_storage import ObjectStorageService
from infrastructure.services.settings_service import get_settings


class DatabaseBackupService:

    @staticmethod
    def run() -> None:
        settings = get_settings()
        backup_prefix = settings.S3_BACKUP_PREFIX
        storage = ObjectStorageService()

        DatabaseBackupService._cleanup_old_backups(storage, backup_prefix)

        pg_url = settings.DATABASE_URL.replace("+asyncpg", "")
        date_str = datetime.utcnow().strftime("%Y%m%d")
        key = f"{backup_prefix}/amonet_{date_str}.dump"

        with tempfile.NamedTemporaryFile(suffix=".dump") as tmp:
            result = subprocess.run(
                ["pg_dump", "--dbname", pg_url, "-Fc", "-Z", "9", "-f", tmp.name],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"pg_dump failed: {result.stderr}")
                return

            tmp.seek(0)
            storage.upload(
                ObjectStorageUploadDto(
                    ruta=backup_prefix,
                    nombre_archivo=f"amonet_{date_str}.dump",
                    archivo=tmp.read(),
                )
            )

        print(f"Database backup uploaded: {key}")

    @staticmethod
    def _cleanup_old_backups(storage: ObjectStorageService, backup_prefix: str) -> None:
        objects = storage.list(ObjectStorageListDto(ruta=backup_prefix), recursive=True)
        cutoff = datetime.utcnow() - timedelta(days=5)

        pattern = re.compile(r"amonet_(\d{8})\.dump$")

        for obj in objects:
            if obj.es_directorio:
                continue

            match = pattern.search(obj.nombre)
            if not match:
                continue

            try:
                backup_date = datetime.strptime(match.group(1), "%Y%m%d")
            except ValueError:
                continue

            if backup_date < cutoff:
                storage.delete(f"{backup_prefix}/{obj.nombre}")
                print(f"Deleted old backup: {obj.nombre}")
