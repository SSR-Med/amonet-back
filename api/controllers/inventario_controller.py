import json
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, require_roles
from Application.Features.Inventario.CreateInventario.command import (
    CreateInventarioCommand,
    CreateInventarioCommandHandler,
)
from Application.Features.Inventario.CreateInventario.dtos import (
    CreateInventarioItemDto,
)
from Application.Features.Inventario.UpdateInventario.command import (
    UpdateInventarioCommand,
    UpdateInventarioCommandHandler,
)
from Application.Features.Inventario.DownloadEvidencia.query import (
    DownloadEvidenciaQuery,
    DownloadEvidenciaQueryHandler,
)
from Application.Features.Inventario.GetAllInventario.query import (
    GetAllInventarioQuery,
    GetAllInventarioQueryHandler,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("/")
async def get_all_inventario(
    query: GetAllInventarioQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllInventarioQueryHandler(session)
    return await handler.handle(query)


@router.get("/evidencia")
async def download_evidencia(
    numero_ingreso: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DownloadEvidenciaQueryHandler(session)
    return await handler.handle(DownloadEvidenciaQuery(numero_ingreso=numero_ingreso))


@router.patch("/{id}")
async def update_inventario(
    id: UUID,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles(["CALIDAD"])),
    archivo: UploadFile = File(None),
    data: str = Form(None),
):
    command = await UpdateInventarioCommand.from_request(request, archivo, data)
    handler = UpdateInventarioCommandHandler(session)
    await handler.handle(id, command, current_user)


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
