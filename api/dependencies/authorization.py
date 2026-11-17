from typing import List

from fastapi import Depends

from api.dependencies.authentication import get_current_user
from core.dtos import CurrentUserDto
from core.exceptions import UnauthorizedException
from core.roles import Role


def require_roles(roles: List[str]):
    if Role.ADMIN in roles:
        raise ValueError("Admin-only endpoints must use require_admin()")

    allowed = {*roles, Role.ADMIN, Role.TODERO}

    async def _check_roles(
        current_user: CurrentUserDto = Depends(get_current_user),
    ) -> CurrentUserDto:
        if current_user.rol not in allowed:
            raise UnauthorizedException(
                f"Access denied. Required roles: {', '.join(roles)}"
            )
        return current_user

    return _check_roles


def require_admin():
    async def _check_admin(
        current_user: CurrentUserDto = Depends(get_current_user),
    ) -> CurrentUserDto:
        if current_user.rol != Role.ADMIN:
            raise UnauthorizedException("Access denied. Required role: ADMIN")
        return current_user

    return _check_admin
