import json
import os
import threading
from datetime import date

from core.constants import LOGS
from core.dtos import AuditLogDto

LOG_LOCK = threading.Lock()


class AuditLogger:
    LOG_DIR = LOGS

    @staticmethod
    def log(entry: AuditLogDto) -> None:
        def _write():
            os.makedirs(AuditLogger.LOG_DIR, exist_ok=True)
            filename = f"{AuditLogger.LOG_DIR}/{date.today().isoformat()}.log"
            line = f"Fecha: {date.today().isoformat()}. Usuario: {entry.usuario}. Feature utilizada: {entry.feature}. Datos: {json.dumps(entry.datos, default=str)}\n"
            with LOG_LOCK:
                with open(filename, "a") as f:
                    f.write(line)

        threading.Thread(target=_write, daemon=True).start()
