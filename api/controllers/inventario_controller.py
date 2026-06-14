import json

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from Application.Features.Inventario.CreateInventario.command import (
    CreateInventarioCommand,
    CreateInventarioCommandHandler,
)
from Application.Features.Inventario.CreateInventario.dtos import (
    CreateInventarioItemDto,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.post("/", status_code=201)
async def create_inventario(
    items: str = Form(...),
    archivo: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    parsed_items = [CreateInventarioItemDto(**item) for item in json.loads(items)]
    archivo_bytes = await archivo.read()

    command = CreateInventarioCommand(
        items=parsed_items,
        archivo=archivo_bytes,
        nombre_archivo=archivo.filename or "file",
    )
    handler = CreateInventarioCommandHandler(session)
    await handler.handle(command, current_user)
