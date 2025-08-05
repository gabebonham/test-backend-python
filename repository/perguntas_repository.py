from sqlalchemy import text
from utils.log_util import LogUtil
from config.sqlalchemy.sqlalchemy_config import engine
from models.pergunta import Pergunta
from datetime import datetime
from typing import Optional

class PerguntaRepository:
    def __init__(self):
        self.con = engine
        self.log = LogUtil().log

        self.queryGetAll = 'SELECT * FROM perguntas ORDER BY ordem {ordem} LIMIT {limit} OFFSET {offset};'
        self.queryGetById = "SELECT * FROM perguntas WHERE id = '{id}';"
        self.queryGetFiltered = (
            "SELECT * FROM perguntas "
            "{where_clause} "
            "ORDER BY ordem {ordem} LIMIT {limit} OFFSET {offset};"
        )
        self.queryDelete = "DELETE FROM perguntas WHERE id = '{id}';"
        self.queryCreate = (
            "INSERT INTO perguntas (idFormulario, titulo, codigo, orientacaoResposta, ordem, obrigatoria, subPergunta, tipoPergunta) "
            "VALUES ('{idFormulario}', '{titulo}', {codigo}, '{orientacaoResposta}', {ordem}, {obrigatoria}, '{subPergunta}', '{tipoPergunta}') RETURNING id;"
        )
        self.queryUpdate = (
            "UPDATE perguntas SET "
            "titulo = '{titulo}', "
            "codigo = {codigo}, "
            "orientacaoResposta = '{orientacaoResposta}', "
            "ordem = {ordem}, "
            "obrigatoria = {obrigatoria}, "
            "subPergunta = '{subPergunta}', "
            "tipoPergunta = '{tipoPergunta}' "
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
        idFormulario: Optional[str] = None,
        titulo: Optional[str] = None,
        codigo: Optional[int] = None,
        orientacaoResposta: Optional[str] = None,
        ordem: Optional[int] = None,
        obrigatoria: Optional[bool] = None,
        subPergunta: Optional[str] = None,
        tipoPergunta: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ):
        try:
            filters = []

            if idFormulario:
                filters.append(f" idFormulario = '{idFormulario}' ")
            if titulo:
                filters.append(f" titulo ILIKE '{titulo}'")
            if codigo is not None:
                filters.append(f" codigo = {codigo} ")
            if orientacaoResposta:
                filters.append(f" orientacaoResposta ILIKE '{orientacaoResposta}' ")
            if obrigatoria is not None:
                filters.append(f" obrigatoria = {'TRUE' if obrigatoria else 'FALSE'} ")
            if subPergunta:
                filters.append(f" subPergunta ILIKE '{subPergunta}' ")
            if tipoPergunta:
                filters.append(f" tipoPergunta ILIKE '{tipoPergunta}' ")

            where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""



            order_str = "DESC"
            if ordem is not None:
                order_str = "ASC"

            query = self.queryGetFiltered.format(
                where_clause=where_clause,
                ordem=order_str,
                limit=limit,
                offset=offset,
            )

            result = self.executeQuery(query)
            return result.fetchall() if result else []

        except Exception as e:
            self.log.error(f'Erro ao buscar perguntas filtradas: {e}')
            return []


    def getAll(self,ordem:str='desc',
               limite: int = 10, 
               offset: int = 0):
        try:
            perguntas = self.executeQuery(self.queryGetAll.format(ordem=(ordem or 'DESC').upper(),limit=limite,offset=offset))
            if perguntas is None:
                return []
            return perguntas.fetchall()
        except Exception as e:
            self.log.error(f'Erro ao buscar todas as perguntas: {e}')
            return []

    def getById(self, id: str):
        try:
            query = self.queryGetById.format(id=id)
            result = self.executeQuery(query)
            return result.fetchone() if result else None
        except Exception as e:
            self.log.error(f'Erro ao buscar pergunta por ID: {e}')
            return None

    def create(self, pergunta: Pergunta):
        try:
            query = self.queryCreate.format(
                idFormulario=pergunta.idformulario,
                titulo=pergunta.titulo,
                codigo=pergunta.codigo,
                orientacaoResposta=pergunta.orientacaoresposta,
                ordem=pergunta.ordem,
                obrigatoria='TRUE' if pergunta.obrigatoria else 'FALSE',
                subPergunta=pergunta.subpergunta,
                tipoPergunta=pergunta.tipopergunta
            )
            self.log.info('Pergunta criada com sucesso.')
            return self.executeQuery(query)
        except Exception as e:
            self.log.error(f'Erro ao criar pergunta: {e}')

    def update(self, pergunta: Pergunta):
        try:
            query = self.queryUpdate.format(
                id=pergunta.id,
                idFormulario=pergunta.idformulario,
                titulo=pergunta.titulo,
                codigo=pergunta.codigo,
                orientacaoResposta=pergunta.orientacaoresposta,
                ordem=pergunta.ordem,
                obrigatoria='TRUE' if pergunta.obrigatoria else 'FALSE',
                subPergunta=pergunta.subpergunta,
                tipoPergunta=pergunta.tipopergunta
            )
            self.executeQuery(query)
            self.log.info('Pergunta atualizada com sucesso.')
        except Exception as e:
            self.log.error(f'Erro ao atualizar pergunta: {e}')

    def delete(self, id: str):
        try:
            perguntaVelha = self.getById(id)
            query = self.queryDelete.format(id=id)
            self.executeQuery(query)
            self.log.info(f'Pergunta com ID {id} deletada com sucesso.')
            return perguntaVelha
        except Exception as e:
            self.log.error(f'Erro ao deletar pergunta: {e}')
