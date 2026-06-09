from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
):
    handler = GetAllMateriaPrimaQueryHandler(session)
    return await handler.handle(query)


@router.post("/", status_code=201)
async def create_materia_prima(
    command: CreateMateriaPrimaCommand,
    session: AsyncSession = Depends(get_async_session),
):
    handler = CreateMateriaPrimaCommandHandler(session)
    return await handler.handle(command)


@router.put("/{id}")
async def update_materia_prima(
    id: UUID,
    command: UpdateMateriaPrimaCommand,
    session: AsyncSession = Depends(get_async_session),
):
    handler = UpdateMateriaPrimaCommandHandler(session)
    command.id = id
    return await handler.handle(command)


@router.delete("/{id}", status_code=204)
async def delete_materia_prima(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    handler = DeleteMateriaPrimaCommandHandler(session)
    await handler.handle(DeleteMateriaPrimaCommand(id=id))


@router.get("/tipos")
async def get_tipos(
    session: AsyncSession = Depends(get_async_session),
):
    handler = GetAllTiposMateriaPrimaQueryHandler(session)
    return await handler.handle(GetAllTiposMateriaPrimaQuery())


@router.get("/tipos_unidad")
async def get_tipos_unidad(
    session: AsyncSession = Depends(get_async_session),
):
    handler = GetAllTiposUnidadQueryHandler(session)
    return await handler.handle(GetAllTiposUnidadQuery())


@router.get("/variables_globales")
async def get_all(
    query: GetAllVariablesGlobalesQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
):
    handler = GetAllVariablesGlobalesQueryHandler(session)
    return await handler.handle(query)


@router.post("/variables_globales", status_code=201)
async def create(
    command: CreateVariablesGlobalesCommand,
    session: AsyncSession = Depends(get_async_session),
):
    handler = CreateVariablesGlobalesCommandHandler(session)
    return await handler.handle(command)


@router.put("/variables_globales/{id}")
async def update(
    id: UUID,
    command: UpdateVariablesGlobalesCommand,
    session: AsyncSession = Depends(get_async_session),
):
    handler = UpdateVariablesGlobalesCommandHandler(session)
    command.id = id
    return await handler.handle(command)


@router.delete("/variables_globales/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    handler = DeleteVariablesGlobalesCommandHandler(session)
    await handler.handle(DeleteVariablesGlobalesCommand(id=id))
