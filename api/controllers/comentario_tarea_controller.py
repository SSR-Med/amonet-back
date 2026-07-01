from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.dtos import CurrentUserDto
from Application.Features.ComentarioTarea.CreateComentarioTarea.command import (
    CreateComentarioTareaCommand,
    CreateComentarioTareaCommandHandler,
)
from Application.Features.ComentarioTarea.DeleteComentarioTarea.command import (
    DeleteComentarioTareaCommand,
    DeleteComentarioTareaCommandHandler,
)
from Application.Features.ComentarioTarea.GetAllComentariosByTarea.query import (
    GetAllComentariosByTareaQuery,
    GetAllComentariosByTareaQueryHandler,
)
from Application.Features.ComentarioTarea.UpdateComentarioTarea.command import (
    UpdateComentarioTareaCommand,
    UpdateComentarioTareaCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/comentarios-tarea", tags=["Comentarios Tarea"])


@router.post("/", status_code=201)
async def create(
    command: CreateComentarioTareaCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreateComentarioTareaCommandHandler(session)
    return await handler.handle(command, current_user)


@router.get("/")
async def get_by_tarea(
    query: GetAllComentariosByTareaQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllComentariosByTareaQueryHandler(session)
    return await handler.handle(query)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DeleteComentarioTareaCommandHandler(session)
    await handler.handle(DeleteComentarioTareaCommand(id=id), current_user)


@router.patch("/{id}")
async def update(
    id: UUID,
    command: UpdateComentarioTareaCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = UpdateComentarioTareaCommandHandler(session)
    return await handler.handle(id, command, current_user)
