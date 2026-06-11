from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import (
    AuthenticationException,
    BadRequestException,
    ConflictException,
    DomainException,
    NotFoundException,
    UnauthorizedException,
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_handler(request: Request, exc: BadRequestException) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(AuthenticationException)
    async def authentication_handler(request: Request, exc: AuthenticationException) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(DomainException)
    async def domain_handler(request: Request, exc: DomainException) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": exc.code, "message": exc.message},
        )
