from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
class Formulario(BaseModel):
    id: Optional[str]  = None
    titulo: str
    descricao: Optional[str]
    ordem: int
    createdat: Optional[datetime] = None