import json
from utils.log_util import LogUtil
from repository.resposta_pergunta_repository import RespostaPerguntaRepository
from models.resposta_pergunta import RespostaPergunta
class RespostaPerguntaService:
    def __init__(self):
        self.log = LogUtil().log
        self.repository = RespostaPerguntaRepository()
        pass
    
    def getAll(self, 
               limite: int = 10, 
               offset: int = 0):
        try:
            return self.repository.getAll(limite,offset)
        except Exception as e:
            self.log.error(e)
    def getById(self, id: str):
        try:
            return self.repository.getById(id)
        except Exception as e:
            self.log.error(e)
    def getFiltered(self, 
                    limit: int = 10, 
                    offset: int = 0,
                    idPergunta: str = None,
                    idOpcaoResposta: str = None):
        try:
            return self.repository.getFiltered(limit,offset,idPergunta,idOpcaoResposta)
        except Exception as e:
            self.log.error(e)
    def create(self, respostaPergunta: RespostaPergunta):
        try:
            result = self.repository.create(respostaPergunta)
            respostaPerguntaNovo = self.getById(result.fetchone()[0])
            return respostaPerguntaNovo
        except Exception as e:
            self.log.error(e)
    def update(self, respostaPergunta: RespostaPergunta):
        try:
            return self.repository.update(respostaPergunta)
        except Exception as e:
            self.log.error(e)
    def delete(self, id:str):
        try:
            respostaPergunta = self.getById(id)
            self.repository.delete(id)
            return respostaPergunta
        except Exception as e:
            self.log.error(e)
    
        