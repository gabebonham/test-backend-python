from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class RespostaPergunta(BaseModel):
    id: Optional[UUID] = None
    idopcaoresposta: Optional[str] = None
    idpergunta: Optional[str] = None
    createdat: Optional[datetime] = None