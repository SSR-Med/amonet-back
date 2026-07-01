from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.dtos import CurrentUserDto
from Application.Features.TareaSprint.CreateTareaSprint.command import (
    CreateTareaSprintCommand,
    CreateTareaSprintCommandHandler,
)
from Application.Features.TareaSprint.DeleteTareaSprint.command import (
    DeleteTareaSprintCommand,
    DeleteTareaSprintCommandHandler,
)
from Application.Features.TareaSprint.GetAllTareasSprint.query import (
    GetAllTareasSprintQuery,
    GetAllTareasSprintQueryHandler,
)
from Application.Features.TareaSprint.GetTareaSprintById.query import (
    GetTareaSprintByIdQuery,
    GetTareaSprintByIdQueryHandler,
)
from Application.Features.TareaSprint.GetTareasBySprint.query import (
    GetTareasBySprintQueryHandler,
)
from Application.Features.TareaSprint.UpdateTareaSprint.command import (
    UpdateTareaSprintCommand,
    UpdateTareaSprintCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/tareas-sprint", tags=["Tareas Sprint"])


@router.get("/")
async def get_all(
    query: GetAllTareasSprintQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllTareasSprintQueryHandler(session)
    return await handler.handle(query)


@router.get("/sprint/{amonet_sprint_id}")
async def get_by_sprint(
    amonet_sprint_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetTareasBySprintQueryHandler(session)
    return await handler.handle(amonet_sprint_id)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetTareaSprintByIdQueryHandler(session)
    return await handler.handle(GetTareaSprintByIdQuery(id=id))


@router.post("/", status_code=201)
async def create(
    command: CreateTareaSprintCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreateTareaSprintCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdateTareaSprintCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = UpdateTareaSprintCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DeleteTareaSprintCommandHandler(session)
    await handler.handle(DeleteTareaSprintCommand(id=id), current_user)
