from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dataaccess.base import Base


class PrioridadKanbanConfiguration(Base):
    __tablename__ = "amonet_prioridad_kanban"
    __table_args__ = (
        UniqueConstraint(
            "color_red", "color_green", "color_blue",
            name="uq_prioridad_kanban_color",
        ),
        CheckConstraint("color_red >= 0 AND color_red <= 255", name="ck_prioridad_kanban_color_red"),
        CheckConstraint("color_green >= 0 AND color_green <= 255", name="ck_prioridad_kanban_color_green"),
        CheckConstraint("color_blue >= 0 AND color_blue <= 255", name="ck_prioridad_kanban_color_blue"),
    )

    id_amonet_prioridad_kanban: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    color_red: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    color_green: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    color_blue: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
