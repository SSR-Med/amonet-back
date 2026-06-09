from uuid import uuid4

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dataaccess.base import Base


class CatalogoTipoUnidadConfiguration(Base):
    __tablename__ = "cat_amonet_tipo_unidad"
    __table_args__ = (
        UniqueConstraint("nombre", "abreviacion"),
    )

    id_cat_amonet_tipo_unidad: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    abreviacion: Mapped[str] = mapped_column(String(20), nullable=False)
