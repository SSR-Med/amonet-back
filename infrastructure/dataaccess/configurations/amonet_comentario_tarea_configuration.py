from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class ComentarioTareaConfiguration(Base):
    __tablename__ = "amonet_comentario_tarea"

    id_amonet_comentario_tarea: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    amonet_tarea_sprint_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("amonet_tarea_sprint.id_amonet_tarea_sprint", ondelete="CASCADE"),
        nullable=False,
    )
    comentario: Mapped[str] = mapped_column(
        Text, nullable=False
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
    fecha_modifica: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    tarea = relationship("TareaSprintConfiguration")
    usuario_alta_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(ComentarioTareaConfiguration.usuario_alta)",
        uselist=False,
    )
