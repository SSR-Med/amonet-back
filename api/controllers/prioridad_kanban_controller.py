from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.dtos import CurrentUserDto
from Application.Features.PrioridadKanban.CreatePrioridadKanban.command import (
    CreatePrioridadKanbanCommand,
    CreatePrioridadKanbanCommandHandler,
)
from Application.Features.PrioridadKanban.DeletePrioridadKanban.command import (
    DeletePrioridadKanbanCommand,
    DeletePrioridadKanbanCommandHandler,
)
from Application.Features.PrioridadKanban.GetAllPrioridadKanban.query import (
    GetAllPrioridadKanbanQuery,
    GetAllPrioridadKanbanQueryHandler,
)
from Application.Features.PrioridadKanban.GetPrioridadKanbanById.query import (
    GetPrioridadKanbanByIdQuery,
    GetPrioridadKanbanByIdQueryHandler,
)
from Application.Features.PrioridadKanban.UpdatePrioridadKanban.command import (
    UpdatePrioridadKanbanCommand,
    UpdatePrioridadKanbanCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/prioridades-kanban", tags=["Prioridades Kanban"])


@router.get("/")
async def get_all(
    query: GetAllPrioridadKanbanQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllPrioridadKanbanQueryHandler(session)
    return await handler.handle(query)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetPrioridadKanbanByIdQueryHandler(session)
    return await handler.handle(GetPrioridadKanbanByIdQuery(id=id))


@router.post("/", status_code=201)
async def create(
    command: CreatePrioridadKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreatePrioridadKanbanCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdatePrioridadKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = UpdatePrioridadKanbanCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DeletePrioridadKanbanCommandHandler(session)
    await handler.handle(DeletePrioridadKanbanCommand(id=id), current_user)
