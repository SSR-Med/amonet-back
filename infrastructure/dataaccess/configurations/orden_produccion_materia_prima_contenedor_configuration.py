from uuid import uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class OrdenProduccionMateriaPrimaContenedorConfiguration(Base):
    __tablename__ = "amonet_orden_produccion_materia_prima_contenedor"
    __table_args__ = (
        UniqueConstraint(
            "amonet_inventario_materia_prima_contenedor_id",
            "amonet_orden_produccion_materia_prima_id",
            name="uq_orden_prod_mat_prima_cont",
        ),
        CheckConstraint("cantidad > 0", name="ck_orden_prod_mat_prima_cont_cantidad"),
        CheckConstraint("coste > 0", name="ck_orden_prod_mat_prima_cont_coste"),
    )

    id_amonet_orden_produccion_materia_prima_contenedor: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    amonet_inventario_materia_prima_contenedor_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_inventario_materia_prima_contenedor.id_amonet_inventario_materia_prima_contenedor",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    amonet_orden_produccion_materia_prima_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_orden_produccion_materia_prima.id_amonet_orden_produccion_materia_prima",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    coste: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)

    orden_produccion_materia_prima = relationship(
        "OrdenProduccionMateriaPrimaConfiguration", back_populates="contenedores"
    )
    inventario_contenedor = relationship("InventarioMateriaPrimaContenedorConfiguration")
