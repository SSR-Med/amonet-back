from sympy import sympify, SympifyError

from core.exceptions import BadRequestException, ConflictException
from core.interfaces import IRepository
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)


class FormulaValidator:

    def __init__(
        self, repo: IRepository[VariablesGlobalesMateriaPrimaConfiguration]
    ) -> None:
        self._repo = repo
        self._variables_cache: set[str] | None = None

    async def _load_variables(self) -> set[str]:
        if self._variables_cache is not None:
            return self._variables_cache

        items, _, _, _ = await self._repo.get_all(page=1, page_size=9999)
        self._variables_cache = {item.nombre for item in items}
        return self._variables_cache

    async def validate(self, formula: str) -> None:
        try:
            expr = sympify(formula)
        except (SympifyError, TypeError, SyntaxError):
            raise BadRequestException(f"Invalid formula expression: '{formula}'")

        symbols = {
            str(s).upper()
            for s in expr.free_symbols
            if not s.is_number
        }

        if not symbols:
            return

        existing = await self._load_variables()

        for symbol in symbols:
            if symbol not in existing:
                raise ConflictException(
                    f"Variable '{symbol}' used in formula does not exist in variables globales"
                )
