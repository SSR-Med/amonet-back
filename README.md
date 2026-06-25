# Amonet — Backend

API REST para gestión de producción de cosméticos.

## Arquitectura

Arquitectura hexagonal (Puertos y Adaptadores) + CQRS + DDD.

```
┌──────────────────────────────────────────────────────┐
│  api/ (FastAPI routers, dependencies, exception handlers, crons)
├──────────────────────────────────────────────────────┤
│  Application/ (CQRS: commands y queries por feature)
├──────────────────────────────────────────────────────┤
│  core/ (domain entities, interfaces/ports, DTOs, exceptions)
├──────────────────────────────────────────────────────┤
│  infrastructure/ (adapters: SQLAlchemy, S3, JWT, bcrypt, APScheduler)
└──────────────────────────────────────────────────────┘
```

- **Core/Dominio:** Entidades puras (dataclasses), interfaces de repositorio y UnitOfWork, excepciones de dominio, DTOs.
- **Aplicación:** Casos de uso organizados por feature. Cada feature separa commands (escritura) de queries (lectura).
- **Infraestructura:** Implementaciones concretas de los puertos (SQLAlchemy, boto3/S3, JWT, bcrypt).
- **API:** Routers FastAPI que delegan en handlers de aplicación. Dependencias de autenticación y autorización.

## Tecnologías

| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.12 | Lenguaje |
| FastAPI | 0.115.6 | Framework web ASGI |
| Uvicorn | 0.34.0 | Servidor ASGI |
| SQLAlchemy | 2.0.36 | ORM asíncrono |
| asyncpg | 0.30.0 | Driver PostgreSQL |
| Pydantic | 2.10.3 | Validación y settings |
| PyJWT | 2.10.1 | Tokens JWT |
| bcrypt | 4.2.1 | Hashing de contraseñas |
| boto3 | 1.35.0 | Cliente S3 |
| APScheduler | 3.10.4 | Tareas programadas |
| sympy | 1.14.0 | Validación de fórmulas |
| PostgreSQL | 16 | Base de datos |

## Funcionalidades

### Módulos

| Módulo | Endpoints | Roles |
|---|---|---|
| **Marcas** | CRUD completo, paginado, filtro por nombre | ADMIN |
| **Productos** | CRUD completo, fórmulas matemáticas con validación sympy | ADMIN |
| **Materias Primas** | CRUD + catálogos (tipos, unidades) + variables globales | ADMIN |
| **Inventario** | Ingresos con evidencia (foto), aprobación/rechazo, descarga de evidencia | OPERARIO crea, CALIDAD aprueba/rechaza |
| **Órdenes de Producción** | Creación con wizard (4 pasos), cambio de estado (finalizar/cancelar con restauración de stock) | JEFE_PRODUCCION crea |
| **Usuarios** | CRUD, login JWT, roles | ADMIN |
| **Logs** | Auditoría, descarga local o desde S3 | ADMIN |

### Autenticación y Autorización

- JWT con HS256. Login retorna token con payload: sub, documento, nombre, rol.
- `HTTPBearer` con esquema `BearerAuth` en Swagger.
- `require_roles()` verifica rol del usuario. ADMIN siempre incluido implícitamente.

### Roles

| Rol | Permisos |
|---|---|
| ADMIN | Acceso total |
| JEFE_PRODUCCION | Crear y gestionar órdenes |
| CALIDAD | Aprobar/rechazar inventario |
| OPERARIO | Lectura, crear ingresos de inventario |

### Tareas Programadas (APScheduler)

| Tarea | Horario | Descripción |
|---|---|---|
| Subida de logs | 00:00 UTC | Archivos de log locales → S3 |
| Backup de BD | 03:00 UTC | pg_dump → S3, limpia backups >5 días |

### Almacenamiento (S3 / Supabase Storage)

- **Evidencias:** Fotos de ingresos de inventario.
- **Backups:** Dumps comprimidos de PostgreSQL (retención 5 días).
- **Logs:** Archivos de log históricos.

### Variables de Entorno

Todas las variables requeridas están documentadas en `.env.example.txt`.
