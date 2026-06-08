from dataclasses import dataclass


@dataclass
class PaginationQuery:
    page: int = 1
    page_size: int = 20
