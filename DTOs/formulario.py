from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from DTOs.pergunta import PerguntaDTO
class FormularioDTO(BaseModel):
    id: Optional[UUID] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    perguntas: List[PerguntaDTO] = None
    ordem: Optional[int] = None 
    createdAt:Optional[datetime] = None
