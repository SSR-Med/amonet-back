from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.configurations import register_exception_handlers
from api.controllers import columna_kanban_router, inventario_router, logs_router, marca_router, materia_prima_router, orden_produccion_router, producto_router, usuario_router
from api.crons import scheduler, setup
from infrastructure.dataaccess import init_db
from infrastructure.services import LogUploader, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    LogUploader.upload_old_logs()
    setup()
    scheduler.start()
    yield
    scheduler.shutdown()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    origins = settings.CORS_ORIGINS.split(",")
    cors_kwargs = {
        "allow_origins": origins if origins != ["*"] else ["*"],
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_credentials": origins != ["*"],
    }

    app.add_middleware(CORSMiddleware, **cors_kwargs)

    register_exception_handlers(app)

    app.include_router(inventario_router, prefix="/api/v1")
    app.include_router(logs_router, prefix="/api/v1")
    app.include_router(marca_router, prefix="/api/v1")
    app.include_router(materia_prima_router, prefix="/api/v1")
    app.include_router(orden_produccion_router, prefix="/api/v1")
    app.include_router(producto_router, prefix="/api/v1")
    app.include_router(usuario_router, prefix="/api/v1")
    app.include_router(columna_kanban_router, prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
