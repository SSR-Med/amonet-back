from typing import Optional

from fastapi import Query

from core.dtos import PaginationQuery


class GetAllVariablesGlobalesQueryDto(PaginationQuery):
    nombre: Optional[str] = Query(None)
