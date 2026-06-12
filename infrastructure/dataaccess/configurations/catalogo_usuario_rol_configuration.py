from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dataaccess.base import Base


class CatalogoUsuarioRolConfiguration(Base):
    __tablename__ = "cat_amonet_usuario_rol"

    id_cat_amonet_usuario_rol: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
