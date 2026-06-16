from typing import List

from fastapi import Depends

from api.dependencies.authentication import get_current_user
from core.constants import ADMIN
from core.dtos import CurrentUserDto
from core.exceptions import UnauthorizedException


def require_roles(roles: List[str]):
    allowed = list(set(roles + [ADMIN]))

    async def _check_roles(
        current_user: CurrentUserDto = Depends(get_current_user),
    ) -> CurrentUserDto:
        if current_user.rol not in allowed:
            raise UnauthorizedException(
                f"Access denied. Required roles: {', '.join(roles)}"
            )
        return current_user

    return _check_roles
