from fastapi import APIRouter, FastAPI
from services.resposta_service import RespostaService
from models.resposta import Resposta
from typing import Optional
from fastapi import Query
from mappers.mapper import obj_to_dict
class RespostasController:
    def __init__(self):
        self.service = RespostaService()
        self.router = APIRouter()
        self.router.get("/respostas/filter", tags=["respostas"])(self.getFiltered)
        self.router.get("/respostas", tags=["respostas"])(self.getAll)
        self.router.get("/respostas/{id}", tags=["respostas"])(self.getById)
        self.router.post("/respostas", tags=["respostas"])(self.create)
        self.router.put("/respostas/{id}", tags=["respostas"])(self.update)
        self.router.delete("/respostas/{id}", tags=["respostas"])(self.delete)

    async def getAll(self,ordem: Optional[str] = Query(None), 
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0)
                     ):
        data = self.service.getAll(ordem, limite, offset)
        print(data)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getFiltered(self,ordem: Optional[str] = Query(None), 
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0),
                     resposta: Optional[str] = Query(None), 
                     idPergunta: Optional[str] = Query(None),
                     respostaAberta:Optional[bool] = Query(False)):
        data = self.service.getFiltered(ordem, limite, offset, idPergunta,resposta,respostaAberta)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getById(self, id:str):
        return obj_to_dict(self.service.getById(id))
    
    async def create(self, resposta:Resposta):
        return obj_to_dict(self.service.create(resposta))
    
    async def delete(self, id:str):
        return obj_to_dict(self.service.delete(id))
    
    async def update(self, resposta:Resposta, id:str):
        resposta.id = id
        return obj_to_dict(self.service.update(resposta))
