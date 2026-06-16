from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, require_roles
from core.constants import ADMIN
from core.dtos import CurrentUserDto
from Application.Features.Marca.GetMarcaById.query import (
    GetMarcaByIdQuery,
    GetMarcaByIdQueryHandler,
)
from Application.Features.Marca.CreateMarca.command import (
    CreateMarcaCommand,
    CreateMarcaCommandHandler,
)
from Application.Features.Marca.DeleteMarca.command import (
    DeleteMarcaCommand,
    DeleteMarcaCommandHandler,
)
from Application.Features.Marca.GetAllMarcas.query import (
    GetAllMarcasQuery,
    GetAllMarcasQueryHandler,
)
from Application.Features.Marca.UpdateMarca.command import (
    UpdateMarcaCommand,
    UpdateMarcaCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/marcas", tags=["Marcas"])


@router.get("/")
async def get_all(
    query: GetAllMarcasQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllMarcasQueryHandler(session)
    return await handler.handle(query)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetMarcaByIdQueryHandler(session)
    return await handler.handle(GetMarcaByIdQuery(id=id))


@router.post("/", status_code=201)
async def create(
    command: CreateMarcaCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = CreateMarcaCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdateMarcaCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = UpdateMarcaCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = DeleteMarcaCommandHandler(session)
    await handler.handle(DeleteMarcaCommand(id=id), current_user)
