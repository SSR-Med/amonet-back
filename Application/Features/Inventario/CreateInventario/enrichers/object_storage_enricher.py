from core.dtos import ObjectStorageUploadDto
from infrastructure.services import ObjectStorageService, get_settings


class ObjectStorageEnricher:

    @staticmethod
    def enrich(archivo: bytes, nombre_archivo: str, numero_ingreso: str) -> str:
        settings = get_settings()
        ruta = f"{settings.S3_EVIDENCIA_PREFIX}/{numero_ingreso}"

        dto = ObjectStorageUploadDto(
            ruta=ruta,
            archivo=archivo,
            nombre_archivo=nombre_archivo,
        )
        ObjectStorageService().upload(dto)

        return f"{ruta}/{nombre_archivo}"
