from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.services import get_settings

engine = None
async_session_maker = None


async def init_db() -> None:
    global engine, async_session_maker
    settings = get_settings()
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"ssl": "require"},
    )
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


async def get_async_session() -> AsyncSession:
    if async_session_maker is None:
        await init_db()
    async with async_session_maker() as session:
        yield session
