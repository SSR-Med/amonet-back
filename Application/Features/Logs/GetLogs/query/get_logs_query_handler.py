import re
from pathlib import Path
from typing import List

from Application.Features.Logs.GetLogs.dtos import LogItemDto
from Application.Features.Logs.GetLogs.mappers import LogMapper
from Application.Features.Logs.GetLogs.query import GetLogsQuery
from core.constants import LOGS
from core.dtos import ObjectStorageListDto, PaginatedResult
from infrastructure.services import ObjectStorageService


class GetLogsQueryHandler:

    def __init__(self) -> None:
        self._storage = ObjectStorageService()

    async def handle(self, query: GetLogsQuery) -> PaginatedResult[LogItemDto]:
        log_map: dict[str, LogItemDto] = {}

        s3_items = self._storage.list(ObjectStorageListDto(ruta=LOGS), recursive=True)
        for item in s3_items:
            if item.es_directorio:
                continue
            key = item.nombre
            parts = key.split("/")
            filename = parts[-1]
            fecha = filename.replace(".log", "")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
                continue
            log_map[filename] = LogItemDto(
                nombre=filename,
                peso=item.peso,
                fecha=fecha,
                origen="s3",
            )

        for filepath in Path(LOGS).glob("*.log"):
            filename = filepath.name
            if filename not in log_map:
                fecha = filename.replace(".log", "")
                if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
                    log_map[filename] = LogItemDto(
                        nombre=filename,
                        peso=filepath.stat().st_size,
                        fecha=fecha,
                        origen="local",
                    )

        items: List[LogItemDto] = [
            i for i in log_map.values()
            if query.fecha_inicio <= i.fecha <= query.fecha_fin
        ]

        items.sort(key=lambda i: i.fecha, reverse=True)

        total = len(items)
        offset = (query.page - 1) * query.page_size
        page_items = items[offset : offset + query.page_size]

        return LogMapper.to_paginated_response(page_items, query.page, total, query.page_size)
