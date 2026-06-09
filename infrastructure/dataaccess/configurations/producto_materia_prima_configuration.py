from uuid import uuid4

from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class ProductoMateriaPrimaConfiguration(Base):
    __tablename__ = "amonet_producto_materia_prima"
    __table_args__ = (
        UniqueConstraint(
            "id_amonet_producto",
            "id_amonet_materia_prima",
            name="uq_producto_materia_prima",
        ),
    )

    id_amonet_producto_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    id_amonet_producto: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_producto.id_amonet_producto", ondelete="CASCADE"),
        nullable=False,
    )
    id_amonet_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_materia_prima.id_amonet_materia_prima",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    formula: Mapped[str] = mapped_column(Text, nullable=True)

    producto = relationship("ProductoConfiguration", backref="materias_primas")
    materia_prima = relationship("MateriaPrimaConfiguration")
