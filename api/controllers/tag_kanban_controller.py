from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.dtos import CurrentUserDto
from Application.Features.TagKanban.CreateTagKanban.command import (
    CreateTagKanbanCommand,
    CreateTagKanbanCommandHandler,
)
from Application.Features.TagKanban.DeleteTagKanban.command import (
    DeleteTagKanbanCommand,
    DeleteTagKanbanCommandHandler,
)
from Application.Features.TagKanban.GetAllTagsKanban.query import (
    GetAllTagsKanbanQuery,
    GetAllTagsKanbanQueryHandler,
)
from Application.Features.TagKanban.GetTagKanbanById.query import (
    GetTagKanbanByIdQuery,
    GetTagKanbanByIdQueryHandler,
)
from Application.Features.TagKanban.UpdateTagKanban.command import (
    UpdateTagKanbanCommand,
    UpdateTagKanbanCommandHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/tags-kanban", tags=["Tags Kanban"])


@router.get("/")
async def get_all(
    query: GetAllTagsKanbanQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllTagsKanbanQueryHandler(session)
    return await handler.handle(query)


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetTagKanbanByIdQueryHandler(session)
    return await handler.handle(GetTagKanbanByIdQuery(id=id))


@router.post("/", status_code=201)
async def create(
    command: CreateTagKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = CreateTagKanbanCommandHandler(session)
    return await handler.handle(command, current_user)


@router.put("/{id}")
async def update(
    id: UUID,
    command: UpdateTagKanbanCommand,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = UpdateTagKanbanCommandHandler(session)
    return await handler.handle(id, command, current_user)


@router.delete("/{id}", status_code=204)
async def delete(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DeleteTagKanbanCommandHandler(session)
    await handler.handle(DeleteTagKanbanCommand(id=id), current_user)
