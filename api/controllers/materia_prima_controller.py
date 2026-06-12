from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, require_roles
from core.constants import ADMIN
from core.dtos import CurrentUserDto
from Application.Features.MateriaPrima.CreateMateriaPrima.command import (
    CreateMateriaPrimaCommand,
    CreateMateriaPrimaCommandHandler,
)
from Application.Features.MateriaPrima.CreateVariablesGlobales.command import (
    CreateVariablesGlobalesCommand,
    CreateVariablesGlobalesCommandHandler,
)
from Application.Features.MateriaPrima.DeleteMateriaPrima.command import (
    DeleteMateriaPrimaCommand,
    DeleteMateriaPrimaCommandHandler,
)
from Application.Features.MateriaPrima.DeleteVariablesGlobales.command import (
    DeleteVariablesGlobalesCommand,
    DeleteVariablesGlobalesCommandHandler,
)
from Application.Features.MateriaPrima.GetAllMateriaPrima.query import (
    GetAllMateriaPrimaQuery,
    GetAllMateriaPrimaQueryHandler,
)
from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.query import (
    GetAllTiposMateriaPrimaQuery,
    GetAllTiposMateriaPrimaQueryHandler,
)
from Application.Features.MateriaPrima.GetAllTiposUnidad.query import (
    GetAllTiposUnidadQuery,
    GetAllTiposUnidadQueryHandler,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.query import (
    GetAllVariablesGlobalesQuery,
    GetAllVariablesGlobalesQueryHandler,
)
from Application.Features.MateriaPrima.UpdateMateriaPrima.command import (
    UpdateMateriaPrimaCommand,
    UpdateMateriaPrimaCommandHandler,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.command import (
    UpdateVariablesGlobalesCommand,
    UpdateVariablesGlobalesCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/materias_primas", tags=["Materia Prima"])


@router.get("/")
async def get_all_materia_prima(
    query: GetAllMateriaPrimaQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllMateriaPrimaQueryHandler(session)
    return await handler.handle(query)


@router.post("/", status_code=201)
async def create_materia_prima(
    command: CreateMateriaPrimaCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = CreateMateriaPrimaCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/{id}")
async def update_materia_prima(
    id: UUID,
    command: UpdateMateriaPrimaCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = UpdateMateriaPrimaCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete_materia_prima(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = DeleteMateriaPrimaCommandHandler(session)
    await handler.handle(DeleteMateriaPrimaCommand(id=id), current_user)


@router.get("/tipos")
async def get_tipos(
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllTiposMateriaPrimaQueryHandler(session)
    return await handler.handle(GetAllTiposMateriaPrimaQuery())


@router.get("/tipos_unidad")
async def get_tipos_unidad(
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllTiposUnidadQueryHandler(session)
    return await handler.handle(GetAllTiposUnidadQuery())


@router.get("/variables_globales")
async def get_all(
    query: GetAllVariablesGlobalesQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllVariablesGlobalesQueryHandler(session)
    return await handler.handle(query)


@router.post("/variables_globales", status_code=201)
async def create(
    command: CreateVariablesGlobalesCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = CreateVariablesGlobalesCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/variables_globales/{id}")
async def update(
    id: UUID,
    command: UpdateVariablesGlobalesCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = UpdateVariablesGlobalesCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/variables_globales/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = DeleteVariablesGlobalesCommandHandler(session)
    await handler.handle(DeleteVariablesGlobalesCommand(id=id), current_user)
