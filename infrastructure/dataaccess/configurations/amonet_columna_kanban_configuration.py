from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, Index, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class ColumnaKanbanConfiguration(Base):
    __tablename__ = "amonet_columna_kanban"
    __table_args__ = (
        Index(
            "uq_columna_kanban_nombre_activo",
            "nombre",
            unique=True,
            postgresql_where=text("activo = true"),
        ),
        CheckConstraint("posicion > 0", name="ck_columna_kanban_posicion"),
    )

    id_amonet_columna_kanban: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    posicion: Mapped[int] = mapped_column(
        nullable=False, unique=True
    )
    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    usuario_alta: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    fecha_alta: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    usuario_modifica: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    fecha_modifica: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    usuario_alta_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(ColumnaKanbanConfiguration.usuario_alta)",
        uselist=False,
    )
    usuario_modifica_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(ColumnaKanbanConfiguration.usuario_modifica)",
        uselist=False,
    )
