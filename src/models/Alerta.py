from src.database.database_manager import DatabaseManager
from datetime import datetime


class Alerta:
    def __init__(self, descricao: str, republica_id: int = None, data_criacao: str = None, id: int = None):
        self.id = id
        self.descricao = descricao
        self.republica_id = republica_id
        self.data_criacao = data_criacao

    def salvar(self):
        db = DatabaseManager()
        if not self.republica_id:
            self.republica_id = self._get_id_republica(db)

        if self.id is None:
            query = """
                INSERT INTO alerta (republica_id, descricao, data_criacao) 
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """
            self.id = db.executar_comando(query, (self.republica_id, self.descricao))
        return self

    def _get_id_republica(self, db):
        res = db.executar_query("SELECT id FROM republica LIMIT 1")
        if res:
            return res[0]['id']
        raise ValueError("Nenhuma república cadastrada para vincular o alerta.")

    @staticmethod
    def buscar_todos():
        db = DatabaseManager()
        query = """
            SELECT id, republica_id, descricao, 
                   strftime('%d/%m/%Y %H:%M', data_criacao) as data_criacao 
            FROM alerta 
            ORDER BY data_criacao DESC
        """
        dados = db.executar_query(query)
        if not dados:
            return []
        return [Alerta(**dado) for dado in dados]

    @staticmethod
    def excluir(alerta_id: int):
        db = DatabaseManager()
        query = "DELETE FROM alerta WHERE id = ?"
        return db.executar_comando(query, (alerta_id,)) > 0