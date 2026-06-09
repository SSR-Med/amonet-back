from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    GetAllVariablesGlobalesQueryDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.query import (
    GetAllVariablesGlobalesQueryHandler,
)
from infrastructure.dataaccess import get_async_session
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository

router = APIRouter(prefix="/materias_primas", tags=["Materia Prima"])


@router.get("/variables_globales")
async def get_all(
    dto: GetAllVariablesGlobalesQueryDto = Query(),
    session: AsyncSession = Depends(get_async_session),
):
    repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)
    handler = GetAllVariablesGlobalesQueryHandler(repository)
    return await handler.handle(dto)
