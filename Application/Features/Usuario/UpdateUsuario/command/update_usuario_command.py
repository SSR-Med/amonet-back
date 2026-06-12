from typing import Optional

from pydantic import BaseModel


class UpdateUsuarioCommand(BaseModel):
    documento: Optional[str] = None
    nombre: Optional[str] = None
    rol: Optional[str] = None
    password: Optional[str] = None
