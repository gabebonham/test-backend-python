from fastapi import APIRouter, FastAPI
from services.perguntas_service import PerguntaService
from models.pergunta import Pergunta
from typing import Optional
from fastapi import Query
from mappers.mapper import obj_to_dict
from uuid import UUID
from datetime import datetime
from typing import Optional
class PerguntaController:
    def __init__(self):
        self.service = PerguntaService()
        self.router = APIRouter()
        self.router.get("/perguntas", tags=["perguntas"])(self.getAll)
        self.router.get("/perguntas/filter", tags=["perguntas"])(self.getFiltered)
        self.router.get("/perguntas/{id}", tags=["perguntas"])(self.getById)
        self.router.post("/perguntas", tags=["perguntas"])(self.create)
        self.router.put("/perguntas/{id}", tags=["perguntas"])(self.update)
        self.router.delete("/perguntas/{id}", tags=["perguntas"])(self.delete)

    async def getAll(self,ordem: Optional[str] = Query('desc'), 
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0)):
        data = self.service.getAll(ordem, limite, offset)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getFiltered(self,
                    idFormulario: Optional[str] = Query(None),
                    titulo: Optional[str] = Query(None),
                    codigo: Optional[int] = Query(None),
                    orientacaoResposta: Optional[str] = Query(None),
                    ordemPergunta: Optional[int] = Query(None),
                    obrigatoria: Optional[bool] = Query(None),
                    subPergunta: Optional[str] = Query(None),
                    tipoPergunta: Optional[str] = Query(None),
                    ordem: Optional[str] = Query("desc"),
                    limite: Optional[int] = Query(10),
                    offset: Optional[int] = Query(0)):
    
        data = self.service.getFiltered(
            idFormulario=idFormulario,
            titulo=titulo,
            codigo=codigo,
            orientacaoResposta=orientacaoResposta,
            ordem=ordemPergunta,
            obrigatoria=obrigatoria,
            subPergunta=subPergunta,
            tipoPergunta=tipoPergunta,
            limit=limite,
            offset=offset,
        )

        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getById(self, id:str):
        return obj_to_dict(self.service.getById(id))
    
    async def create(self, pergunta:Pergunta):
        return obj_to_dict(self.service.create(pergunta))
    
    async def delete(self, id:str):
        return obj_to_dict(self.service.delete(id))
    
    async def update(self, pergunta:Pergunta, id:str):
        pergunta.id = id
        return obj_to_dict(self.service.update(pergunta))
