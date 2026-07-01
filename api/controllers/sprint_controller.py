from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.dtos import CurrentUserDto
from Application.Features.Sprint.CreateSprint.command import (
    CreateSprintCommand,
    CreateSprintCommandHandler,
)
from Application.Features.Sprint.DeleteSprint.command import (
    DeleteSprintCommand,
    DeleteSprintCommandHandler,
)
from Application.Features.Sprint.GetAllSprints.query import (
    GetAllSprintsQuery,
    GetAllSprintsQueryHandler,
)
from Application.Features.Sprint.GetSprintById.query import (
    GetSprintByIdQuery,
    GetSprintByIdQueryHandler,
)
from Application.Features.Sprint.UpdateSprint.command import (
    UpdateSprintCommand,
    UpdateSprintCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/sprints", tags=["Sprints"])


@router.get("/")
async def get_all(
    query: GetAllSprintsQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllSprintsQueryHandler(session)
    return await handler.handle(query)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetSprintByIdQueryHandler(session)
    return await handler.handle(GetSprintByIdQuery(id=id))


@router.post("/", status_code=201)
async def create(
    command: CreateSprintCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreateSprintCommandHandler(session)
    return await handler.handle(command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DeleteSprintCommandHandler(session)
    await handler.handle(DeleteSprintCommand(id=id), current_user)


@router.patch("/{id}")
async def update(
    id: UUID,
    command: UpdateSprintCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = UpdateSprintCommandHandler(session)
    return await handler.handle(id, command, current_user)
