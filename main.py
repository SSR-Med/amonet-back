import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from api.configurations import register_exception_handlers
from api.controllers import columna_kanban_router, comentario_tarea_router, inventario_router, logs_router, marca_router, materia_prima_router, orden_produccion_router, prioridad_kanban_router, producto_router, sprint_router, tag_kanban_router, tarea_sprint_router, usuario_router
from api.crons import scheduler, setup
from api.dependencies.rate_limiter import limiter
from infrastructure.dataaccess import init_db
from infrastructure.services import LogUploader, get_settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    LogUploader.upload_old_logs()
    await setup()
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

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_handler)

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response

    register_exception_handlers(app)

    app.include_router(inventario_router, prefix="/api/v1")
    app.include_router(logs_router, prefix="/api/v1")
    app.include_router(marca_router, prefix="/api/v1")
    app.include_router(materia_prima_router, prefix="/api/v1")
    app.include_router(orden_produccion_router, prefix="/api/v1")
    app.include_router(producto_router, prefix="/api/v1")
    app.include_router(usuario_router, prefix="/api/v1")
    app.include_router(columna_kanban_router, prefix="/api/v1")
    app.include_router(comentario_tarea_router, prefix="/api/v1")
    app.include_router(sprint_router, prefix="/api/v1")
    app.include_router(prioridad_kanban_router, prefix="/api/v1")
    app.include_router(tag_kanban_router, prefix="/api/v1")
    app.include_router(tarea_sprint_router, prefix="/api/v1")

    return app


def _rate_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "RATE_LIMIT_EXCEEDED", "message": str(exc.detail)},
    )


app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
