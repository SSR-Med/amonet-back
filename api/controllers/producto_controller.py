from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
)
from Application.Features.Producto.GetAllProductos.query import (
    GetAllProductosQueryHandler,
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
):
    handler = CreateProductoCommandHandler(session)
    return await handler.handle(command)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    handler = DeleteProductoCommandHandler(session)
    await handler.handle(DeleteProductoCommand(id=id))
