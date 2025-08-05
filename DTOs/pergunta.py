from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from DTOs.resposta import RespostaDTO
class PerguntaDTO(BaseModel):
    id: Optional[UUID] = None
    idformulario: Optional[UUID]= None
    titulo: Optional[str] = None
    codigo: Optional[int] = None
    orientacaoresposta: Optional[str] = None
    ordem: Optional[int] = None
    obrigatoria: bool = None
    subpergunta: Optional[str] = None
    createdat: Optional[datetime] = None
    tipopergunta: Optional[str] = None
    respostas: Optional[List[RespostaDTO]] = []


