from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class TareaSprintConfiguration(Base):
    __tablename__ = "amonet_tarea_sprint"
    __table_args__ = (
        UniqueConstraint(
            "posicion",
            "amonet_sprint_id",
            "amonet_columna_kanban_id",
            name="uq_tarea_sprint_posicion_sprint_columna",
        ),
        CheckConstraint("posicion >= 0", name="ck_tarea_sprint_posicion"),
    )

    id_amonet_tarea_sprint: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    titulo: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    descripcion: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    posicion: Mapped[int] = mapped_column(
        nullable=False
    )
    amonet_sprint_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_sprint.id_amonet_sprint", ondelete="CASCADE"),
        nullable=False,
    )
    amonet_columna_kanban_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_columna_kanban.id_amonet_columna_kanban", ondelete="CASCADE"),
        nullable=False,
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

    sprint = relationship("SprintConfiguration")
    columna = relationship("ColumnaKanbanConfiguration")
    usuario_alta_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(TareaSprintConfiguration.usuario_alta)",
        uselist=False,
    )
    usuario_modifica_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(TareaSprintConfiguration.usuario_modifica)",
        uselist=False,
    )
