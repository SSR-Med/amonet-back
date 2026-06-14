from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class InventarioMateriaPrimaConfiguration(Base):
    __tablename__ = "amonet_inventario_materia_prima"

    id_amonet_inventario_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    fecha_ingreso: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    numero_ingreso: Mapped[str] = mapped_column(String(50), nullable=False)
    amonet_materia_prima_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_materia_prima.id_amonet_materia_prima", ondelete="CASCADE"),
        nullable=False,
    )
    proveedor: Mapped[str] = mapped_column(String(255), nullable=False)
    lote: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_vencimiento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    usuario_alta: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    usuario_modifica: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    ruta_evidencia: Mapped[str] = mapped_column(Text, nullable=False)

    materia_prima = relationship("MateriaPrimaConfiguration")
    usuario_alta_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(InventarioMateriaPrimaConfiguration.usuario_alta)",
        uselist=False,
    )
    contenedores: Mapped[List["InventarioMateriaPrimaContenedorConfiguration"]] = relationship(
        back_populates="inventario"
    )
