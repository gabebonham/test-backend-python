import json
from utils.log_util import LogUtil
from repository.formulario_repository import FormularioRepository
from services.perguntas_service import PerguntaService
from models.formulario import Formulario
from mappers.mapper import map_formulario_to_dto, map_formulario_to_dto_no_pergunta
class FormularioService:
    def __init__(self):
        self.log = LogUtil().log
        self.repository = FormularioRepository()
        self.service = PerguntaService()
        pass
    
    def getAll(self, ordem:str='desc',
               limite: int = 10, 
               offset: int = 0):
        try:
            formulariosDto = []
            formularios = self.repository.getAll(ordem,limite,offset) or []
            for formulario in formularios:
                perguntas = self.service.getFiltered(idFormulario=formulario.id) or []
                formularioDto = map_formulario_to_dto_no_pergunta(formulario, perguntas)
                formulariosDto.append(formularioDto)
            return formulariosDto
        except Exception as e:
            self.log.error(e)
    def getById(self, id: str):
        try:
            return self.repository.getById(id)
        except Exception as e:
            self.log.error(e)
    def getFiltered(self, ordem: str = 'desc', limit: int = 10, offset: int = 0, titulo:str=None, descricao:str=None):
        try:
            return self.repository.getFiltered(ordem,limit,offset,titulo,descricao)
        except Exception as e:
            self.log.error(e)
    def create(self, formulario: Formulario):
        try:
            result = self.repository.create(formulario)
            formularioNovo = self.getById(result.fetchone()[0])
            return formularioNovo
        except Exception as e:
            self.log.error(e)
    def update(self, formulario: Formulario):
        try:
            return self.repository.update(formulario)
        except Exception as e:
            self.log.error(e)
    def delete(self, id:str):
        try:
            formulario = self.getById(id)
            self.repository.delete(id)
            return formulario
        except Exception as e:
            self.log.error(e)
    
        