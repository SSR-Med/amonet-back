import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.services import get_settings
from infrastructure.services.password_service import PasswordService


async def seed() -> None:
    settings = get_settings()
    admin_documento = os.getenv("SEED_ADMIN_DOCUMENTO", "admin")
    admin_password = os.getenv("SEED_ADMIN_PASSWORD")
    admin_rol = os.getenv("SEED_ADMIN_ROL", "ADMIN")

    if not admin_password:
        print("SEED_ADMIN_PASSWORD not set, skipping.")
        return

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
    )

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        result = await session.execute(
            select(UsuarioConfiguration).where(
                UsuarioConfiguration.documento == admin_documento
            )
        )
        existing = result.scalar_one_or_none()

        if existing is not None:
            print(f"Admin user '{admin_documento}' already exists (id={existing.id_amonet_usuario})")
            return

        from uuid import uuid4

        user = UsuarioConfiguration(
            id_amonet_usuario=uuid4(),
            documento=admin_documento,
            nombre=admin_documento.upper(),
            rol=admin_rol,
            password=PasswordService.hash(admin_password),
            activo=True,
        )
        session.add(user)
        await session.commit()
        print(f"Admin user created: {admin_documento}")


if __name__ == "__main__":
    asyncio.run(seed())
