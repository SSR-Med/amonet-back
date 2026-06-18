from uuid import uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class OrdenProduccionVariableGlobalConfiguration(Base):
    __tablename__ = "amonet_orden_produccion_variable_global"
    __table_args__ = (
        UniqueConstraint(
            "amonet_orden_produccion_id",
            "amonet_variable_materia_prima_id",
            name="uq_orden_prod_var_global",
        ),
        CheckConstraint("cantidad > 0", name="ck_orden_prod_var_global_cantidad"),
    )

    id_amonet_orden_produccion_variable_global: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    amonet_orden_produccion_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_orden_produccion.id_amonet_orden_produccion",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    amonet_variable_materia_prima_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "amonet_variable_materia_prima.id_amonet_variable_materia_prima",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    orden_produccion = relationship(
        "OrdenProduccionConfiguration", back_populates="variables_globales"
    )
    variable_materia_prima = relationship("VariablesGlobalesMateriaPrimaConfiguration")
