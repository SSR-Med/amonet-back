from uuid import uuid4

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class OrdenProduccionMateriaPrimaConfiguration(Base):
    __tablename__ = "amonet_orden_produccion_materia_prima"
    __table_args__ = (
        UniqueConstraint(
            "amonet_materia_prima_id",
            "amonet_orden_produccion_id",
            name="uq_orden_prod_materia_prima",
        ),
    )

    id_amonet_orden_produccion_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    amonet_materia_prima_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_materia_prima.id_amonet_materia_prima",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    amonet_orden_produccion_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_orden_produccion.id_amonet_orden_produccion",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    orden_produccion = relationship(
        "OrdenProduccionConfiguration", back_populates="materias_primas"
    )
    materia_prima = relationship("MateriaPrimaConfiguration")
    contenedores = relationship(
        "OrdenProduccionMateriaPrimaContenedorConfiguration",
        back_populates="orden_produccion_materia_prima",
    )
