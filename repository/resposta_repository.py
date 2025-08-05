from sqlalchemy import text
from utils.log_util import LogUtil
from config.sqlalchemy.sqlalchemy_config import engine
from models.resposta import Resposta
from datetime import datetime

class RespostaRepository:
    def __init__(self,):
        self.con = engine
        self.log = LogUtil().log

        self.queryGetAll = 'SELECT * FROM respostas ORDER BY ordem {ordem} LIMIT {limit} OFFSET {offset};'
        self.queryGetById = "SELECT * FROM respostas WHERE id = '{id}';"
        self.queryDelete = "DELETE FROM respostas WHERE id = '{id}';"
        self.queryGetFiltered = (
            "SELECT * FROM respostas "
            "{where_clause} "
            "ORDER BY ordem {ordem} LIMIT {limit} OFFSET {offset};"
        )
        self.queryCreate = (
            "INSERT INTO respostas (idPergunta, resposta, ordem, respostaAberta) "
            "VALUES ('{idPergunta}', '{resposta}', {ordem}, {respostaAberta}) RETURNING id;"
        )
        self.queryUpdate = (
            "UPDATE respostas SET "
            "resposta = '{resposta}', "
            "ordem = {ordem}, "
            "respostaAberta = {respostaAberta} "
            "WHERE id = '{id}';"
        )
    def getFiltered(
            self,
            ordem: str = 'desc',
            limit: int = 10,
            offset: int = 0,
            idPergunta: str = None,
            resposta: str = None,
            respostaAberta: bool = False
        ):
            try:
                filters = []
                if idPergunta:
                    filters.append(f"idPergunta = '{idPergunta}'")

                if resposta:
                    filters.append(f"resposta ILIKE '{resposta}'")
                if respostaAberta:
                    filters.append(f"respostaAberta = '{respostaAberta}'")
                where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

                query = self.queryGetFiltered.format(
                    where_clause=where_clause,
                    ordem=(ordem or 'DESC').upper(),
                    limit=limit,
                    offset=offset
                )

                resposta = self.executeQuery(query)
                if resposta is None:
                    return []

                return resposta.fetchall()

            except Exception as e:
                self.log.error(f'Erro ao buscar respostas filtradss: {e}')
                return []
    

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

    def getAll(self,
            ordem: str = 'desc',
            limite: int = 10,
            offset: int = 0):
        try:
            respostas = self.executeQuery(self.queryGetAll.format(ordem=(ordem or 'DESC').upper(),limit=limite,offset=offset))
            if respostas is None:
                return []
            return respostas.fetchall()
        except Exception as e:
            self.log.error(f'Erro ao buscar todas as respostas: {e}')
            return []

    def getById(self, id: str):
        try:
            query = self.queryGetById.format(id=id)
            result = self.executeQuery(query)
            return result.fetchone() if result else None
        except Exception as e:
            self.log.error(f'Erro ao buscar resposta por ID: {e}')
            return None

    def create(self, resposta: Resposta):
        try:
            query = self.queryCreate.format(
                idPergunta=resposta.idpergunta,
                resposta=resposta.resposta,
                ordem=resposta.ordem,
                respostaAberta='TRUE' if resposta.respostaaberta else 'FALSE',
            )
            self.log.info('Resposta criada com sucesso.')
            return self.executeQuery(query)
            
        except Exception as e:
            self.log.error(f'Erro ao criar resposta: {e}')

    def update(self, resposta: Resposta):
        try:
            query = self.queryUpdate.format(
                id=resposta.id,
                idPergunta=resposta.idpergunta,
                resposta=resposta.resposta,
                ordem=resposta.ordem,
                respostaAberta='TRUE' if resposta.respostaaberta else 'FALSE',
            )
            self.executeQuery(query)
            self.log.info('Resposta atualizada com sucesso.')
        except Exception as e:
            self.log.error(f'Erro ao atualizar resposta: {e}')

    def delete(self, id: str):
        try:
            respostaVelha = self.getById(id)
            query = self.queryDelete.format(id=id)
            self.executeQuery(query)
            self.log.info(f'Resposta com ID {id} deletada com sucesso.')
            return respostaVelha
        except Exception as e:
            self.log.error(f'Erro ao deletar resposta: {e}')
