from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Identity, Index, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class SprintConfiguration(Base):
    __tablename__ = "amonet_sprint"
    __table_args__ = (
        Index(
            "uq_sprint_principal",
            "principal",
            unique=True,
            postgresql_where=text("principal = true"),
        ),
    )

    id_amonet_sprint: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    contador: Mapped[int] = mapped_column(
        Integer, Identity(always=False, start=1, increment=1)
    )
    fecha_inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    principal: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    descripcion: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    usuario_alta: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    usuario_modifica: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    fecha_modifica: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    usuario_alta_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(SprintConfiguration.usuario_alta)",
        uselist=False,
    )
    usuario_modifica_rel = relationship(
        "UsuarioConfiguration",
        primaryjoin="UsuarioConfiguration.id_amonet_usuario == foreign(SprintConfiguration.usuario_modifica)",
        uselist=False,
    )
