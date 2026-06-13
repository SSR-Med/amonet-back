from typing import List

import boto3
from botocore.config import Config

from core.dtos import (
    ObjectStorageDownloadDto,
    ObjectStorageItemDto,
    ObjectStorageListDto,
    ObjectStorageUploadDto,
)
from infrastructure.services.settings_service import get_settings


class ObjectStorageService:

    def __init__(self) -> None:
        settings = get_settings()
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version="s3v4"),
        )
        self._bucket = settings.S3_BUCKET

    def upload(self, dto: ObjectStorageUploadDto) -> None:
        key = f"{dto.ruta}/{dto.nombre_archivo}" if dto.ruta else dto.nombre_archivo
        self._client.put_object(Bucket=self._bucket, Key=key, Body=dto.archivo)

    def list(self, dto: ObjectStorageListDto) -> List[ObjectStorageItemDto]:
        prefix = f"{dto.ruta}/" if dto.ruta else ""
        resp = self._client.list_objects_v2(
            Bucket=self._bucket, Prefix=prefix, Delimiter="/"
        )

        items: List[ObjectStorageItemDto] = []
        for folder in resp.get("CommonPrefixes", []):
            items.append(
                ObjectStorageItemDto(nombre=folder["Prefix"], es_directorio=True)
            )
        for obj in resp.get("Contents", []):
            nombre = obj["Key"].replace(prefix, "")
            if nombre:
                items.append(
                    ObjectStorageItemDto(
                        nombre=nombre, es_directorio=False, peso=obj["Size"]
                    )
                )
        return items

    def get_download_url(self, dto: ObjectStorageDownloadDto) -> str:
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": dto.ruta},
            ExpiresIn=3600,
        )
