from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class Pergunta(BaseModel):
    id: Optional[UUID] = None
    idformulario: Optional[str] = None
    titulo: Optional[str] = None
    codigo: Optional[int] = None
    orientacaoresposta: Optional[str] = None
    ordem: Optional[int] = None
    obrigatoria: Optional[bool] = None
    subpergunta: Optional[str] = None
    createdat: Optional[datetime] = None
    tipopergunta: Optional[str] = None
