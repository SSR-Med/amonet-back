from uuid import uuid4

from sqlalchemy import Boolean, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dataaccess.base import Base


class UsuarioConfiguration(Base):
    __tablename__ = "amonet_usuario"

    id_amonet_usuario: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    documento: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default=text("'OPERARIO'")
    )
    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
