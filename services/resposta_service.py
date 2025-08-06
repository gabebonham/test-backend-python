import json
from utils.log_util import LogUtil
from repository.resposta_repository import RespostaRepository
from services.resposta_pergunta_service import RespostaPerguntaService
from models.resposta import Resposta
class RespostaService:
    def __init__(self):
        self.log = LogUtil().log
        self.repository = RespostaRepository()
        self.service = RespostaPerguntaService()
        pass
    
    def getAll(self, ordem:str='desc',
               limite: int = 10, 
               offset: int = 0):
        try:
            respostas = self.repository.getAll(ordem,limite,offset)
            for resposta in respostas:
                vezesrespondidas = len(self.service.getFiltered(idOpcaoResposta=resposta.id))
                if vezesrespondidas:
                    resposta.vezesrespondidas = vezesrespondidas
            return respostas
        except Exception as e:
            self.log.error(e)
    def getById(self, id: str):
        try:
            resposta = self.repository.getById(id)
            vezesrespondidas = len(self.service.getFiltered(idOpcaoResposta=resposta.id))
            if vezesrespondidas:
                resposta.vezesrespondidas = vezesrespondidas
            
            return resposta
        except Exception as e:
            self.log.error(e)
    def getFiltered(self, ordem: str = 'desc', 
                    limit: int = 10, 
                    offset: int = 0,
                    idPergunta: str = None,
                    resposta: str = None,
                    respostaAberta: bool = False):
        try:
            return self.repository.getFiltered(ordem,limit,offset,idPergunta,resposta,respostaAberta)
        except Exception as e:
            self.log.error(e)
    def create(self, resposta: Resposta):
        try:
            result = self.repository.create(resposta)
            respostaNova = self.getById(result.fetchone()[0])
            return respostaNova
        except Exception as e:
            self.log.error(e)
    def update(self, resposta: Resposta):
        try:
            return self.repository.update(resposta)
        except Exception as e:
            self.log.error(e)
    def delete(self, id:str):
        try:
            resposta = self.getById(id)
            self.repository.delete(id)
            return resposta
        except Exception as e:
            self.log.error(e)
    
        