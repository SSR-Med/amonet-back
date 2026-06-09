from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dataaccess.base import Base


class VariablesGlobalesMateriaPrimaConfiguration(Base):
    __tablename__ = "amonet_variable_materia_prima"

    id_amonet_variable_materia_prima: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
