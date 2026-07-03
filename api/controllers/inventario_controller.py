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
from Application.Features.Inventario.GetInventarioById.query import (
    GetInventarioByIdQuery,
    GetInventarioByIdQueryHandler,
)
from Application.Features.Inventario.DownloadEvidencia.query import (
    DownloadEvidenciaQuery,
    DownloadEvidenciaQueryHandler,
)
from Application.Features.Inventario.GetAllInventario.query import (
    GetAllInventarioQuery,
    GetAllInventarioQueryHandler,
)
from core.constants import CALIDAD
from core.dtos import CurrentUserDto
from infrastructure.dataaccess import get_async_session
from infrastructure.services import get_settings

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("/evidencia")
async def download_evidencia(
    numero_ingreso: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = DownloadEvidenciaQueryHandler(session)
    return await handler.handle(DownloadEvidenciaQuery(numero_ingreso=numero_ingreso))


@router.get("/")
async def get_all_inventario(
    query: GetAllInventarioQuery = Query(),
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetAllInventarioQueryHandler(session)
    return await handler.handle(query)


@router.get("/{id}")
async def get_inventario_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(get_current_user),
):
    handler = GetInventarioByIdQueryHandler(session)
    return await handler.handle(GetInventarioByIdQuery(id=id))


@router.patch("/{id}")
async def update_inventario(
    id: UUID,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: CurrentUserDto = Depends(require_roles([CALIDAD])),
    archivo: UploadFile = File(None),
    data: str = Form(None),
):
    if archivo is not None:
        max_size = get_settings().UPLOAD_MAX_SIZE_MB * 1024 * 1024
        content = await archivo.read(max_size + 1)
        if len(content) > max_size:
            from core.exceptions import BadRequestException
            raise BadRequestException(f"El archivo excede el tamaño máximo de {get_settings().UPLOAD_MAX_SIZE_MB} MB")
        await archivo.seek(0)
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
    max_size = get_settings().UPLOAD_MAX_SIZE_MB * 1024 * 1024
    archivo_bytes = await archivo.read(max_size + 1)
    if len(archivo_bytes) > max_size:
        from core.exceptions import BadRequestException
        raise BadRequestException(f"El archivo excede el tamaño máximo de {get_settings().UPLOAD_MAX_SIZE_MB} MB")

    command = CreateInventarioCommand(
        items=parsed_items,
        archivo=archivo_bytes,
        nombre_archivo=archivo.filename or "file",
    )
    handler = CreateInventarioCommandHandler(session)
    await handler.handle(command, current_user)
