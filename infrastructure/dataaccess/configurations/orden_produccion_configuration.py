from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class OrdenProduccionConfiguration(Base):
    __tablename__ = "amonet_orden_produccion"
    __table_args__ = (
        CheckConstraint("coste >= 0", name="ck_orden_produccion_coste"),
    )

    id_amonet_orden_produccion: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    observacion_creacion: Mapped[str] = mapped_column(Text, nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    amonet_producto_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_producto.id_amonet_producto", ondelete="CASCADE"),
        nullable=False,
    )
    fecha_alta: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    usuario_alta: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    fecha_modifica: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    usuario_modifica: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    amonet_estado_produccion_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "cat_amonet_estado_produccion.id_cat_amonet_estado_produccion",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    coste: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    cancel_razon_descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    producto = relationship("ProductoConfiguration")
    estado_produccion = relationship("CatalogoEstadoProduccionConfiguration")
    usuario_alta_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(OrdenProduccionConfiguration.usuario_alta)",
        uselist=False,
    )
    usuario_modifica_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(OrdenProduccionConfiguration.usuario_modifica)",
        uselist=False,
    )
    variables_globales = relationship(
        "OrdenProduccionVariableGlobalConfiguration",
        back_populates="orden_produccion",
    )
    materias_primas = relationship(
        "OrdenProduccionMateriaPrimaConfiguration",
        back_populates="orden_produccion",
    )
