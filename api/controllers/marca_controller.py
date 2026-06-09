from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
):
    handler = GetAllMarcasQueryHandler(session)
    return await handler.handle(query)


@router.post("/", status_code=201)
async def create(
    command: CreateMarcaCommand,
    session: AsyncSession = Depends(get_async_session),
):
    handler = CreateMarcaCommandHandler(session)
    return await handler.handle(command)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdateMarcaCommand,
    session: AsyncSession = Depends(get_async_session),
):
    handler = UpdateMarcaCommandHandler(session)
    command.id = id
    return await handler.handle(command)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    handler = DeleteMarcaCommandHandler(session)
    await handler.handle(DeleteMarcaCommand(id=id))
