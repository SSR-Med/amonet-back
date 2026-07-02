from typing import List
from uuid import UUID

from pydantic import BaseModel


class ReorderItem(BaseModel):
    id: UUID
    posicion: int


class ReorderColumnasKanbanCommand(BaseModel):
    items: List[ReorderItem]
