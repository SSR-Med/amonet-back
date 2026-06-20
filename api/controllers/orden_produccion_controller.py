from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from Application.Features.OrdenProduccion.CreateOrdenProduccion.command import (
    CreateOrdenProduccionCommand,
    CreateOrdenProduccionCommandHandler,
)
from Application.Features.OrdenProduccion.GetAllEstadosProduccion.query import (
    GetAllEstadosProduccionQuery,
    GetAllEstadosProduccionQueryHandler,
)
from Application.Features.OrdenProduccion.GetAllOrdenesProduccion.query import (
    GetAllOrdenesProduccionQuery,
    GetAllOrdenesProduccionQueryHandler,
)
from Application.Features.OrdenProduccion.GetOrdenProduccionById.query import (
    GetOrdenProduccionByIdQuery,
    GetOrdenProduccionByIdQueryHandler,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/ordenes_produccion", tags=["Ordenes Produccion"])


@router.get("/")
async def get_all(
    query: GetAllOrdenesProduccionQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllOrdenesProduccionQueryHandler(session)
    return await handler.handle(query)


@router.get("/estados")
async def get_estados(
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllEstadosProduccionQueryHandler(session)
    return await handler.handle(GetAllEstadosProduccionQuery())


@router.post("/", status_code=201)
async def create(
    command: CreateOrdenProduccionCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreateOrdenProduccionCommandHandler(session)
    return await handler.handle(command, current_user)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetOrdenProduccionByIdQueryHandler(session)
    return await handler.handle(GetOrdenProduccionByIdQuery(id=id))
