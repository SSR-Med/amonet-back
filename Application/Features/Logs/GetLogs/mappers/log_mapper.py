from typing import List

from Application.Features.Logs.GetLogs.dtos import LogItemDto
from core.dtos import PaginatedResult


class LogMapper:

    @staticmethod
    def to_paginated_response(
        items: List[LogItemDto],
        page: int,
        total: int,
        page_size: int,
    ) -> PaginatedResult[LogItemDto]:
        return PaginatedResult(
            items=items,
            current_page=page,
            total_items=total,
            page_size=page_size,
        )
