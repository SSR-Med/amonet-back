from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.Login.query import (
    LoginQuery,
    LoginQueryHandler,
)
from infrastructure.dataaccess import get_async_session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/login")
async def login(
    query: LoginQuery,
    session: AsyncSession = Depends(get_async_session),
):
    handler = LoginQueryHandler(session)
    return await handler.handle(query)
