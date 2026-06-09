from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.configurations import register_exception_handlers
from api.controllers import marca_router, materia_prima_router, producto_router
from infrastructure.dataaccess import init_db
from infrastructure.services import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    register_exception_handlers(app)

    app.include_router(marca_router, prefix="/api/v1")
    app.include_router(materia_prima_router, prefix="/api/v1")
    app.include_router(producto_router, prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
