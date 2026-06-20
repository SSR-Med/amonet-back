from uuid import uuid4

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.dataaccess.base import Base


class MateriaPrimaConfiguration(Base):
    __tablename__ = "amonet_materia_prima"

    id_amonet_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    id_cat_amonet_tipo_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "cat_amonet_tipo_materia_prima.id_cat_amonet_tipo_materia_prima",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    id_cat_amonet_tipo_unidad: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "cat_amonet_tipo_unidad.id_cat_amonet_tipo_unidad",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    tipo_materia_prima = relationship("CatalogoTipoMateriaPrimaConfiguration")
    tipo_unidad = relationship("CatalogoTipoUnidadConfiguration")
