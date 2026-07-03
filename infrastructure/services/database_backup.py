import asyncio
import re
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone

from core.dtos import ObjectStorageListDto, ObjectStorageUploadDto
from infrastructure.services.object_storage import ObjectStorageService
from infrastructure.services.settings_service import get_settings


class DatabaseBackupService:

    @staticmethod
    async def run() -> None:
        settings = get_settings()
        backup_prefix = settings.S3_BACKUP_PREFIX
        storage = ObjectStorageService()

        await DatabaseBackupService._cleanup_old_backups(storage, backup_prefix)

        pg_url = settings.DATABASE_URL.replace("+asyncpg", "")
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        key = f"{backup_prefix}/amonet_{date_str}.dump"

        loop = asyncio.get_running_loop()
        with tempfile.NamedTemporaryFile(suffix=".dump") as tmp:
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    ["pg_dump", "--dbname", pg_url, "-Fc", "-Z", "9", "-f", tmp.name],
                    capture_output=True,
                    text=True,
                ),
            )

            if result.returncode != 0:
                print(f"pg_dump failed: {result.stderr}")
                return

            tmp.seek(0)
            file_content = await loop.run_in_executor(None, tmp.read)
            storage.upload(
                ObjectStorageUploadDto(
                    ruta=backup_prefix,
                    nombre_archivo=f"amonet_{date_str}.dump",
                    archivo=file_content,
                )
            )

        print(f"Database backup uploaded: {key}")

    @staticmethod
    async def _cleanup_old_backups(storage: ObjectStorageService, backup_prefix: str) -> None:
        settings = get_settings()
        objects = storage.list(ObjectStorageListDto(ruta=backup_prefix), recursive=True)
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.S3_BACKUP_RETENTION_DAYS)

        pattern = re.compile(r"amonet_(\d{8})\.dump$")

        for obj in objects:
            if obj.es_directorio:
                continue

            match = pattern.search(obj.nombre)
            if not match:
                continue

            try:
                backup_date = datetime.strptime(match.group(1), "%Y%m%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue

            if backup_date < cutoff:
                storage.delete(f"{backup_prefix}/{obj.nombre}")
                print(f"Deleted old backup: {obj.nombre}")
