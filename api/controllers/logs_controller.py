from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, RedirectResponse

from api.dependencies import require_roles
from Application.Features.Logs.DownloadLog.query import (
    DownloadLogQuery,
    DownloadLogQueryHandler,
)
from Application.Features.Logs.GetLogs.query import (
    GetLogsQuery,
    GetLogsQueryHandler,
)
from core.constants import ADMIN
from core.dtos import CurrentUserDto

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/")
async def get_logs(
    query: GetLogsQuery = Query(),
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = GetLogsQueryHandler()
    return await handler.handle(query)


@router.get("/download")
async def download_log(
    nombre: str,
    current_user: CurrentUserDto = Depends(require_roles([ADMIN])),
):
    handler = DownloadLogQueryHandler()
    result = await handler.handle(DownloadLogQuery(nombre=nombre))

    if result is None:
        raise HTTPException(status_code=404, detail="Log file not found")

    if result.origen == "s3":
        return RedirectResponse(url=result.presigned_url)

    return FileResponse(
        path=str(result.local_path),
        filename=result.nombre,
        media_type="text/plain",
    )
