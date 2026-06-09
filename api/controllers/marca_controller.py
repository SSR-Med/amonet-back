from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Marca.CreateMarca.command import (
    CreateMarcaCommandHandler,
)
from Application.Features.Marca.CreateMarca.dtos import (
    CreateMarcaCommandDto,
)
from Application.Features.Marca.DeleteMarca.command import (
    DeleteMarcaCommandHandler,
)
from Application.Features.Marca.DeleteMarca.dtos import (
    DeleteMarcaCommand,
)
from Application.Features.Marca.GetAllMarcas.dtos import (
    GetAllMarcasQueryDto,
)
from Application.Features.Marca.GetAllMarcas.query import (
    GetAllMarcasQueryHandler,
)
from Application.Features.Marca.UpdateMarca.command import (
    UpdateMarcaCommandHandler,
)
from Application.Features.Marca.UpdateMarca.dtos import (
    UpdateMarcaCommandDto,
)
from infrastructure.dataaccess import get_async_session
from infrastructure.dataaccess.configurations import MarcaConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork

router = APIRouter(prefix="/marcas", tags=["Marcas"])


@router.get("/")
async def get_all(
    dto: GetAllMarcasQueryDto = Query(),
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, MarcaConfiguration)
    handler = GetAllMarcasQueryHandler(repository)
    return await handler.handle(dto)


@router.post("/", status_code=201)
async def create(
    dto: CreateMarcaCommandDto,
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, MarcaConfiguration)
    unit_of_work = UnitOfWork(session)
    handler = CreateMarcaCommandHandler(repository, unit_of_work)
    return await handler.handle(dto)


@router.put("/{id}")
async def update(
    id: UUID,
    dto: UpdateMarcaCommandDto,
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, MarcaConfiguration)
    unit_of_work = UnitOfWork(session)
    handler = UpdateMarcaCommandHandler(repository, unit_of_work)
    dto.id = id
    return await handler.handle(dto)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, MarcaConfiguration)
    unit_of_work = UnitOfWork(session)
    handler = DeleteMarcaCommandHandler(repository, unit_of_work)
    await handler.handle(DeleteMarcaCommand(id=id))
