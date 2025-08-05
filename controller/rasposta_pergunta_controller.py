from fastapi import APIRouter, FastAPI
from services.resposta_pergunta_service import RespostaPerguntaService
from models.resposta_pergunta import RespostaPergunta
from typing import Optional
from fastapi import Query
from mappers.mapper import obj_to_dict
class RespostaPerguntaController:
    def __init__(self):
        self.service = RespostaPerguntaService()
        self.router = APIRouter()
        self.router.get("/respostas-perguntas", tags=["respostas-perguntas"])(self.getAll)
        self.router.get("/respostas-perguntas/{id}", tags=["respostas-perguntas"])(self.getById)
        self.router.post("/respostas-perguntas", tags=["respostas-perguntas"])(self.create)
        self.router.put("/respostas-perguntas", tags=["respostas-perguntas"])(self.update)
        self.router.delete("/respostas-perguntas/{id}", tags=["respostas-perguntas"])(self.delete)

    async def getAll(self,
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0)
                     ):
        data = self.service.getAll(limite, offset)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getFiltered(self,
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0),
                     idOpcaoResposta: Optional[str] = Query(None), 
                     idPergunta: Optional[str] = Query(None)):
        data = self.service.getFiltered(limite, offset,idOpcaoResposta, idPergunta)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getById(self, id:str):
        return obj_to_dict(self.service.getById(id))
    
    async def create(self, respostaPergunta:RespostaPergunta):
        return obj_to_dict(self.service.create(respostaPergunta))
    
    async def delete(self, id:str):
        return obj_to_dict(self.service.delete(id))
    
    async def update(self, respostaPergunta:RespostaPergunta):
        return obj_to_dict(self.service.update(respostaPergunta))
