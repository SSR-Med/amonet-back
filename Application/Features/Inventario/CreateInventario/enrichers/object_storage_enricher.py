import re

from core.dtos import ObjectStorageUploadDto
from infrastructure.services import ObjectStorageService, get_settings

_PATH_SAFE_RE = re.compile(r"[^a-zA-Z0-9_.\-]")


class ObjectStorageEnricher:

    @staticmethod
    def enrich(archivo: bytes, nombre_archivo: str, numero_ingreso: str) -> str:
        settings = get_settings()
        safe_numero = _PATH_SAFE_RE.sub("_", numero_ingreso)
        safe_nombre = _PATH_SAFE_RE.sub("_", nombre_archivo)
        ruta = f"{settings.S3_EVIDENCIA_PREFIX}/{safe_numero}"

        dto = ObjectStorageUploadDto(
            ruta=ruta,
            archivo=archivo,
            nombre_archivo=safe_nombre,
        )
        ObjectStorageService().upload(dto)

        return f"{ruta}/{safe_nombre}"
