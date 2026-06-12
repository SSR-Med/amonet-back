from dataclasses import dataclass


@dataclass
class AuditLogDto:
    usuario: str
    feature: str
    datos: dict
