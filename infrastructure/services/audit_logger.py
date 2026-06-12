import json
import os
from datetime import date

from core.dtos import AuditLogDto


class AuditLogger:
    LOG_DIR = "logs"

    @staticmethod
    def log(entry: AuditLogDto) -> None:
        os.makedirs(AuditLogger.LOG_DIR, exist_ok=True)
        filename = f"{AuditLogger.LOG_DIR}/{date.today().isoformat()}.log"
        line = f"Fecha: {date.today().isoformat()}. Usuario: {entry.usuario}. Feature utilizada: {entry.feature}. Datos: {json.dumps(entry.datos, default=str)}\n"
        with open(filename, "a") as f:
            f.write(line)
