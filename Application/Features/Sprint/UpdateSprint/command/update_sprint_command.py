from typing import Optional

from pydantic import BaseModel


class UpdateSprintCommand(BaseModel):
    principal: Optional[bool] = None
    descripcion: Optional[str] = None
