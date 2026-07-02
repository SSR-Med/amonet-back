from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.dtos import CurrentUserDto
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.command import (
    CreateColumnaKanbanCommand,
    CreateColumnaKanbanCommandHandler,
)
from Application.Features.ColumnaKanbanBoard.GetAllColumnaKanban.query import (
    GetAllColumnaKanbanQuery,
    GetAllColumnaKanbanQueryHandler,
)
from Application.Features.ColumnaKanbanBoard.GetColumnaKanbanById.query import (
    GetColumnaKanbanByIdQuery,
    GetColumnaKanbanByIdQueryHandler,
)
from Application.Features.ColumnaKanbanBoard.DeleteColumnaKanban.command import (
    DeleteColumnaKanbanCommand,
    DeleteColumnaKanbanCommandHandler,
)
from Application.Features.ColumnaKanbanBoard.UpdateColumnaKanban.command import (
    UpdateColumnaKanbanCommand,
    UpdateColumnaKanbanCommandHandler,
)
from Application.Features.ColumnaKanbanBoard.ReorderColumnasKanban.command import (
    ReorderColumnasKanbanCommand,
    ReorderColumnasKanbanCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/columnas-kanban", tags=["Columnas Kanban"])


@router.get("/")
async def get_all(
    query: GetAllColumnaKanbanQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllColumnaKanbanQueryHandler(session)
    return await handler.handle(query)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetColumnaKanbanByIdQueryHandler(session)
    return await handler.handle(GetColumnaKanbanByIdQuery(id=id))


@router.post("/", status_code=201)
async def create(
    command: CreateColumnaKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreateColumnaKanbanCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/orden")
async def reorder(
    command: ReorderColumnasKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = ReorderColumnasKanbanCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdateColumnaKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = UpdateColumnaKanbanCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DeleteColumnaKanbanCommandHandler(session)
    await handler.handle(DeleteColumnaKanbanCommand(id=id), current_user)
