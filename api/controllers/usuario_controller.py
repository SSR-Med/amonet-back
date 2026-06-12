from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, require_roles
from core.constants import ADMIN
from core.dtos import CurrentUserDto
from Application.Features.Usuario.GetCurrentUsuario.query import (
    GetCurrentUsuarioQuery,
    GetCurrentUsuarioQueryHandler,
)
from Application.Features.Usuario.CreateUsuario.command import (
    CreateUsuarioCommand,
    CreateUsuarioCommandHandler,
)
from Application.Features.Usuario.DeleteUsuario.command import (
    DeleteUsuarioCommand,
    DeleteUsuarioCommandHandler,
)
from Application.Features.Usuario.UpdateUsuario.command import (
    UpdateUsuarioCommand,
    UpdateUsuarioCommandHandler,
)
from Application.Features.Usuario.GetAllRoles.query import (
    GetAllRolesQuery,
    GetAllRolesQueryHandler,
)
from Application.Features.Usuario.GetAllUsuarios.query import (
    GetAllUsuariosQuery,
    GetAllUsuariosQueryHandler,
)
from Application.Features.Usuario.Login.query import (
    LoginQuery,
    LoginQueryHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", status_code=201)
async def create(
    command: CreateUsuarioCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = CreateUsuarioCommandHandler(session)
    return await handler.handle(command, current_user)


@router.get("/me")
async def get_current(
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetCurrentUsuarioQueryHandler(session)
    return await handler.handle(GetCurrentUsuarioQuery(), current_user)


@router.get("/roles")
async def get_all_roles(
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllRolesQueryHandler(session)
    return await handler.handle(GetAllRolesQuery())


@router.get("/")
async def get_all(
    query: GetAllUsuariosQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = GetAllUsuariosQueryHandler(session)
    return await handler.handle(query)


@router.patch("/{id}")
async def update(
    id: UUID,
    command: UpdateUsuarioCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = UpdateUsuarioCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    command = DeleteUsuarioCommand(id=id)
    handler = DeleteUsuarioCommandHandler(session)
    await handler.handle(command, current_user)


@router.post("/login")
async def login(
    query: LoginQuery,
    session: AsyncSession = Depends(get_async_session),
):
    handler = LoginQueryHandler(session)
    return await handler.handle(query)
