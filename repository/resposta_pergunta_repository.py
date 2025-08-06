from sqlalchemy import text
from utils.log_util import LogUtil
from config.sqlalchemy.sqlalchemy_config import engine
from models.resposta_pergunta import RespostaPergunta
from datetime import datetime

class RespostaPerguntaRepository:
    def __init__(self,):
        self.con = engine
        self.log = LogUtil().log

        self.queryGetAll = 'SELECT * FROM respostas_pergunta LIMIT {limit} OFFSET {offset};'
        self.queryGetById = "SELECT * FROM respostas_pergunta WHERE id = '{id}';"
        self.queryDelete = "DELETE FROM respostas_pergunta WHERE id = '{id}';"
        self.queryGetFiltered = (
            "SELECT * FROM respostas_pergunta "
            " {where_clause} "
            " LIMIT {limit} OFFSET {offset};"
        )
        self.queryCreate = (
            "INSERT INTO respostas_pergunta (idOpcaoResposta, idPergunta) "
            "VALUES ( '{idopcaoresposta}', '{idpergunta}') RETURNING id;"
        )
        self.queryUpdate = (
            "UPDATE respostas_pergunta SET "
            "idOpcaoResposta = '{idopcaoresposta}', "
            "idPergunta = '{idpergunta}', "
            "WHERE id = '{id}';"
        )

    def executeQuery(self, query:str):
        try:
            self.log.info(f'Executando query {query}')
            result = None
            with self.con.connect() as conn:
                with conn.begin(): 
                    result = conn.execute(text(query))
            if not result:
                self.log.info('Query sem retorno')
            else:
                self.log.info('Query com retorno')
                
            return result
        except Exception as e:
            self.log.error(f'Erro ao executar query: {e}')
            return None
    def getFiltered(
            self,
            limit: int = 10,
            offset: int = 0,
            idPergunta: str = None,
            idOpcaoResposta: str = None
        ):
            try:
                filters = []

                if idPergunta:
                    filters.append(f"idPergunta = '{idPergunta}'")

                if idOpcaoResposta:
                    filters.append(f"idOpcaoResposta = '{idOpcaoResposta}'")

                where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

                query = self.queryGetFiltered.format(
                    where_clause=where_clause,
                    limit=limit,
                    offset=offset,
                )

                results = self.executeQuery(query)
                if results is None:
                    return []
                return results.fetchall()

            except Exception as e:
                self.log.error(f'Erro ao buscar Resposta_Pergunta filtrados: {e}')
                return []

    def getAll(self,
            limite: int = 10,
            offset: int = 0):
        try:
            respostas = self.executeQuery(self.queryGetAll.format(limit=limite,offset=offset))
            if respostas is None:
                return []
            return respostas.fetchall()
        except Exception as e:
            self.log.log(f'Erro ao buscar todas as respostas: {e}')
            return []

    def getById(self, id: str):
        try:
            query = self.queryGetById.format(id=id)
            result = self.executeQuery(query)
            return result.fetchone() if result else None
        except Exception as e:
            self.log.error(f'Erro ao buscar resposta por ID: {e}')
            return None

    def create(self, resposta: RespostaPergunta):
        try:
            query = self.queryCreate.format(
                idopcaoresposta=resposta.idopcaoresposta,
                idpergunta=resposta.idpergunta,
            )
            self.log.info('Resposta criada com sucesso.')
            return self.executeQuery(query)
        except Exception as e:
            self.log.error(f'Erro ao criar resposta: {e}')

    def update(self, resposta: RespostaPergunta):
        try:
            query = self.queryUpdate.format(
                id=resposta.id,
                idopcaoresposta=resposta.idopcaoresposta,
                idpergunta=resposta.idpergunta,
                createdat=resposta.createdat.isoformat()
            )
            self.executeQuery(query)
            self.log.info('Resposta atualizada com sucesso.')
        except Exception as e:
            self.log.error(f'Erro ao atualizar resposta: {e}')

    def delete(self, id: str):
        try:
            resultadoVelho = self.getById(id)
            query = self.queryDelete.format(id=id)
            self.executeQuery(query)
            self.log.info(f'Resposta com ID {id} deletada com sucesso.')
            return resultadoVelho
        except Exception as e:
            self.log.error(f'Erro ao deletar resposta: {e}')
