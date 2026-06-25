from .cron_setup import CronSetup

_cron = CronSetup()
scheduler = _cron.scheduler
setup = _cron.register_jobs
