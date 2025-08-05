from fastapi import APIRouter, FastAPI
from services.formulario_service import FormularioService
from models.formulario import Formulario
from typing import Optional
from fastapi import Query
from mappers.mapper import obj_to_dict
class FormulariosController:
    def __init__(self):
        self.service = FormularioService()
        self.router = APIRouter()
        self.router.get("/formularios", tags=["formularios"])(self.getAll)
        self.router.get("/formularios/filter", tags=["formularios"])(self.getFiltered)
        self.router.get("/formularios/{id}", tags=["formularios"])(self.getById)
        self.router.post("/formularios", tags=["formularios"])(self.create)
        self.router.put("/formularios/{id}", tags=["formularios"])(self.update)
        self.router.delete("/formularios/{id}", tags=["formularios"])(self.delete)

    async def getAll(self,ordem: Optional[str] = Query('desc'), 
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0)):
        data = self.service.getAll(ordem, limite, offset)
        print(data)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getFiltered(self,ordem: Optional[str] = Query(None), 
                     limite: Optional[int] = Query(10),
                     offset: Optional[int] = Query(0),
                     titulo: Optional[str] = Query(None), 
                     descricao: Optional[str] = Query(None)):
        data = self.service.getFiltered(ordem, limite, offset,titulo, descricao)
        lista = [obj_to_dict(row) for row in data]
        return lista
    async def getById(self, id:str):
        return obj_to_dict(self.service.getById(id))
    
    async def create(self, formulario:Formulario):
        return obj_to_dict(self.service.create(formulario))
    
    async def delete(self, id:str):
        return obj_to_dict(self.service.delete(id))
    
    async def update(self, formulario:Formulario, id:str):
        formulario.id = id
        return obj_to_dict(self.service.update(formulario))
