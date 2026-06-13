from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.services import LogUploader

scheduler = AsyncIOScheduler()


def setup_cron_jobs() -> None:
    scheduler.add_job(
        LogUploader.upload_old_logs,
        trigger="cron",
        hour=0,
        minute=0,
        id="upload_logs_daily",
    )
