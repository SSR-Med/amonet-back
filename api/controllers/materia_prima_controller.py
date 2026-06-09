from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.CreateVariablesGlobales.command import (
    CreateVariablesGlobalesCommandHandler,
)
from Application.Features.MateriaPrima.CreateVariablesGlobales.dtos import (
    CreateVariablesGlobalesCommandDto,
)
from Application.Features.MateriaPrima.DeleteVariablesGlobales.command import (
    DeleteVariablesGlobalesCommandHandler,
)
from Application.Features.MateriaPrima.GetAllTiposMateriaPrima.query import (
    GetAllTiposMateriaPrimaQueryHandler,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    GetAllVariablesGlobalesQueryDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.query import (
    GetAllVariablesGlobalesQueryHandler,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.command import (
    UpdateVariablesGlobalesCommandHandler,
)
from Application.Features.MateriaPrima.UpdateVariablesGlobales.dtos import (
    UpdateVariablesGlobalesCommandDto,
)
from infrastructure.dataaccess import get_async_session
from infrastructure.dataaccess.configurations import (
    CatalogoTipoMateriaPrimaConfiguration,
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork

router = APIRouter(prefix="/materias_primas", tags=["Materia Prima"])


@router.get("/tipos")
async def get_tipos(
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, CatalogoTipoMateriaPrimaConfiguration)
    handler = GetAllTiposMateriaPrimaQueryHandler(repository)
    return await handler.handle()


@router.get("/variables_globales")
async def get_all(
    dto: GetAllVariablesGlobalesQueryDto = Query(),
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)
    handler = GetAllVariablesGlobalesQueryHandler(repository)
    return await handler.handle(dto)


@router.post("/variables_globales", status_code=201)
async def create(
    dto: CreateVariablesGlobalesCommandDto,
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)
    unit_of_work = UnitOfWork(session)
    handler = CreateVariablesGlobalesCommandHandler(repository, unit_of_work)
    return await handler.handle(dto)


@router.put("/variables_globales/{id}")
async def update(
    id: UUID,
    dto: UpdateVariablesGlobalesCommandDto,
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)
    unit_of_work = UnitOfWork(session)
    handler = UpdateVariablesGlobalesCommandHandler(repository, unit_of_work)
    return await handler.handle(id, dto)


@router.delete("/variables_globales/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)
    unit_of_work = UnitOfWork(session)
    handler = DeleteVariablesGlobalesCommandHandler(repository, unit_of_work)
    await handler.handle(id)
