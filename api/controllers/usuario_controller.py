from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, require_roles
from core.constants import ADMIN
from Application.Features.Usuario.GetAllUsuarios.query import (
    GetAllUsuariosQuery,
    GetAllUsuariosQueryHandler,
)
from Application.Features.Usuario.Login.query import (
    LoginQuery,
    LoginQueryHandler,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/")
async def get_all(
    query: GetAllUsuariosQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = GetAllUsuariosQueryHandler(session)
    return await handler.handle(query)


@router.post("/login")
async def login(
    query: LoginQuery,
    session: AsyncSession = Depends(get_async_session),
):
    handler = LoginQueryHandler(session)
    return await handler.handle(query)
