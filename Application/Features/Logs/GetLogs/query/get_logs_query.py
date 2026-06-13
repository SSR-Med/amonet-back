from core.dtos import PaginationQuery


class GetLogsQuery(PaginationQuery):
    fecha_inicio: str
    fecha_fin: str
