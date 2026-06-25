from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.services import LogUploader
from infrastructure.services.database_backup import DatabaseBackupService


class CronSetup:

    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()

    @property
    def scheduler(self) -> AsyncIOScheduler:
        return self._scheduler

    def register_jobs(self) -> None:
        self._scheduler.add_job(
            LogUploader.upload_old_logs,
            trigger="cron",
            hour=0,
            minute=0,
            id="upload_logs_daily",
        )

        self._scheduler.add_job(
            DatabaseBackupService().run,
            trigger="cron",
            hour=3,
            minute=0,
            id="database_backup_daily",
        )
