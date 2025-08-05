from sqlalchemy import text
from utils.log_util import LogUtil
from config.sqlalchemy.sqlalchemy_config import engine
from models.formulario import Formulario

class FormularioRepository:
    def __init__(self):
        self.con = engine
        self.log = LogUtil().log
        self.queryGetAll = 'SELECT * FROM formularios ORDER BY ordem {ordem} LIMIT {limit} OFFSET {offset};'
        self.queryGetFiltered = (
            "SELECT * FROM formularios "
            "{where_clause} "
            "ORDER BY ordem {ordem} LIMIT {limit} OFFSET {offset};"
        )
        self.queryGetById = "SELECT * FROM formularios WHERE id = '{id}';"
        self.queryDelete = "DELETE FROM formularios WHERE id = '{id}';"
        self.queryCreate = (
            "INSERT INTO formularios ( titulo, descricao, ordem) "
            "VALUES ('{titulo}', '{descricao}', '{ordem}' ) RETURNING id;"
        )
        self.queryUpdate = (
            "UPDATE formularios SET "
            "titulo = '{titulo}', descricao = '{descricao}', ordem = {ordem} "
            "WHERE id = '{id}';"
        )
        pass
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
        ordem: str = 'desc',
        limit: int = 10,
        offset: int = 0,
        titulo: str = None,
        descricao: str = None
    ):
        try:
            filters = []

            if titulo:
                filters.append(f"titulo ILIKE '%{titulo}%'")

            if descricao:
                filters.append(f"descricao ILIKE '%{descricao}%'")

            where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

            query = self.queryGetFiltered.format(
                where_clause=where_clause,
                ordem=(ordem or 'DESC').upper(),
                limit=limit,
                offset=offset
            )

            formularios = self.executeQuery(query)
            if formularios is None:
                return []

            return formularios.fetchall()

        except Exception as e:
            self.log.error(f'Erro ao buscar formulários filtrados: {e}')
            return []

    def getAll(self,
           ordem: str = 'desc',
           limite: int = 10,
           offset: int = 0):
        try:
            
            formularios = self.executeQuery(self.queryGetAll.format(ordem=(ordem or 'DESC').upper(), limit=limite, offset=offset))
            
            if formularios is None:
                return []
            return formularios.fetchall()

        except Exception as e:
            self.log.error(f'Erro ao buscar todos formularios: {e}')
            return []

    def getById(self, id: str):
        try:
            query = self.queryGetById.format(id=id)
            result = self.executeQuery(query)
            return result.fetchone() if result else None
        except Exception as e:
            self.log.error(f'Erro ao buscar formulário por ID: {e}')
            return None
    def create(self, formulario: Formulario):
        try:
            query = self.queryCreate.format(
                titulo=formulario.titulo,
                descricao=formulario.descricao,
                ordem=formulario.ordem,
            )
            self.log.info('Formulário criado com sucesso.')
            return self.executeQuery(query)
        except Exception as e:
            self.log.error(f'Erro ao criar formulário: {e}')
    def update(self, formulario: Formulario):
        try:
            query = self.queryUpdate.format(
                titulo=formulario.titulo,
                descricao=formulario.descricao,
                ordem=formulario.ordem,
                id=formulario.id
            )
            self.executeQuery(query)
            self.log.info('Formulário atualizado com sucesso.')
        except Exception as e:
            self.log.error(f'Erro ao atualizar formulário: {e}')

    def delete(self, id: str):
        try:
            query = self.queryDelete.format(id=id)
            self.executeQuery(query)
            self.log.info(f'Formulário com ID {id} deletado com sucesso.')
        except Exception as e:
            self.log.error(f'Erro ao deletar formulário: {e}')