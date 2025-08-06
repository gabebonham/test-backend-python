from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class Resposta(BaseModel):
    id: Optional[UUID] = None
    idpergunta: Optional[str] = None
    resposta: Optional[str] = None
    ordem: Optional[int] = None
    respostaaberta: Optional[bool] = None
    vezesrespondidas: Optional[list] = None
    createdat: Optional[datetime] = None