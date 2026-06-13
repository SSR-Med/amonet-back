from dataclasses import dataclass
from typing import Optional


@dataclass
class ObjectStorageUploadDto:
    ruta: str
    archivo: bytes
    nombre_archivo: str


@dataclass
class ObjectStorageItemDto:
    nombre: str
    es_directorio: bool
    peso: Optional[int] = None


@dataclass
class ObjectStorageListDto:
    ruta: Optional[str] = None


@dataclass
class ObjectStorageDownloadDto:
    ruta: str
