from typing import Optional

from pydantic import BaseModel


class CreateSprintCommand(BaseModel):
    descripcion: Optional[str] = None
