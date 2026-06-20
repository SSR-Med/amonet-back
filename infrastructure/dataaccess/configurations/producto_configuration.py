from uuid import uuid4

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class ProductoConfiguration(Base):
    __tablename__ = "amonet_producto"

    id_amonet_producto: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    codigo: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    id_amonet_marca: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_marca.id_amonet_marca", ondelete="CASCADE"),
        nullable=False,
    )

    marca = relationship("MarcaConfiguration")
