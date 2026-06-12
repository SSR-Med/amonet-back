from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import require_roles
from core.constants import ADMIN
from core.dtos import CurrentUserDto
from Application.Features.Producto.CreateProducto.command import (
    CreateProductoCommand,
    CreateProductoCommandHandler,
)
from Application.Features.Producto.DeleteProducto.command import (
    DeleteProductoCommand,
    DeleteProductoCommandHandler,
)
from Application.Features.Producto.GetAllProductos.query import (
    GetAllProductosQuery,
    GetAllProductosQueryHandler,
)
from Application.Features.Producto.UpdateProducto.command import (
    UpdateProductoCommand,
    UpdateProductoCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/")
async def get_all(
    query: GetAllProductosQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
):
    handler = GetAllProductosQueryHandler(session)
    return await handler.handle(query)


@router.post("/", status_code=201)
async def create(
    command: CreateProductoCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = CreateProductoCommandHandler(session)
    return await handler.handle(command)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdateProductoCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = UpdateProductoCommandHandler(session)
    return await handler.handle(id, command)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = DeleteProductoCommandHandler(session)
    await handler.handle(DeleteProductoCommand(id=id))
