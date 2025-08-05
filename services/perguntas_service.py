import json
from utils.log_util import LogUtil
from repository.perguntas_repository import PerguntaRepository
from services.resposta_service import RespostaService
from models.pergunta import Pergunta
from mappers.mapper import map_to_pergunta_dto
class PerguntaService:
    def __init__(self):
        self.log = LogUtil().log
        self.repository = PerguntaRepository()
        self.service = RespostaService()
        pass
    
    def getAll(self, ordem:str='desc',
               limite: int = 10, 
               offset: int = 0):
        try:
            perguntasDto = []
            perguntas = self.repository.getAll(ordem,limite,offset) or []
            for pergunta in perguntas:
                respostas = self.service.getFiltered(idPergunta=pergunta.id) or []
                perguntaDto = map_to_pergunta_dto(pergunta, respostas)
                perguntasDto.append(perguntaDto)
            return perguntasDto
        except Exception as e:
            self.log.error(e)
    def getById(self, id: str):
        try:
            return self.repository.getById(id)
        except Exception as e:
            self.log.error(e)
    def getFiltered(self, ordem: str = 'desc', 
                    limit: int = 10, 
                    offset: int = 0,
                    idFormulario: str | None = None,
                    titulo: str | None = None,
                    codigo: int | None = None,
                    orientacaoResposta: str | None = None,
                    obrigatoria: bool | None = None,
                    subPergunta: str | None = None,
                    tipoPergunta: str | None = None):
        try:
            perguntasDto = []
            perguntas = self.repository.getFiltered(idFormulario,
                                               titulo,
                                               codigo,
                                               orientacaoResposta,
                                               ordem,
                                               obrigatoria,
                                               subPergunta,
                                               tipoPergunta,
                                               limit,
                                               offset)
            for pergunta in perguntas:
                respostas = self.service.getFiltered(idPergunta=pergunta.id) or []
                perguntaDto = map_to_pergunta_dto(pergunta, respostas)
                perguntasDto.append(perguntaDto)
            return perguntasDto
        except Exception as e:
            self.log.error(e)
    def create(self, pergunta: Pergunta):
        try:
            result = self.repository.create(pergunta)
            perguntaNova = self.getById(result.fetchone()[0])
            return perguntaNova
        except Exception as e:
            self.log.error(e)
    def update(self, pergunta: Pergunta):
        try:
            return self.repository.update(pergunta)
        except Exception as e:
            self.log.error(e)
    def delete(self, id:str):
        try:
            pergunta = self.getById(id)
            self.repository.delete(id)
            return pergunta
        except Exception as e:
            self.log.error(e)
    
        