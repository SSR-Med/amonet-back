from uuid import uuid4

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class InventarioMateriaPrimaContenedorConfiguration(Base):
    __tablename__ = "amonet_inventario_materia_prima_contenedor"

    id_amonet_inventario_materia_prima_contenedor: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    contador_materia_prima: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    precio: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    amonet_inventario_materia_prima_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_inventario_materia_prima.id_amonet_inventario_materia_prima",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    inventario = relationship("InventarioMateriaPrimaConfiguration", back_populates="contenedores")
