from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class RespostaPergunta(BaseModel):
    id: Optional[UUID] = None
    idOpcaoResposta: Optional[str] = None
    idPergunta: Optional[str] = None
    createdAt: Optional[datetime] = None