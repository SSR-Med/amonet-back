from typing import Any, Callable, List, Optional


class QueryBuilder:

    def __init__(self) -> None:
        self._filters: List[Any] = []

    def and_filter(self, condition: Any) -> "QueryBuilder":
        self._filters.append(condition)
        return self

    def and_if_not_none(
        self, value: Optional[Any], condition_factory: Callable[[], Any]
    ) -> "QueryBuilder":
        if value is not None:
            self._filters.append(condition_factory())
        return self

    def and_if_not_empty(
        self, value: Optional[str], condition_factory: Callable[[], Any]
    ) -> "QueryBuilder":
        if value is not None and value != "":
            self._filters.append(condition_factory())
        return self

    def build(self) -> Callable:
        if not self._filters:
            return lambda q: q
        return lambda q: q.where(*self._filters)
