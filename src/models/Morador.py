from __future__ import annotations
from .usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import Optional, List

class Morador(Usuario):
    def __init__(self, **kwargs):
        kwargs['tipo_usuario'] = 'morador'
        super().__init__(**kwargs)

    def salvar(self): pass
    def atualizar(self): pass
    def excluir(self): pass

    @staticmethod
    def buscar_todos() -> List[Morador]:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE tipo_usuario = 'morador' ORDER BY nome"
        resultados = db_manager.executar_query(query)
        return [Morador(**r) for r in resultados]

    @staticmethod
    def buscar_por_cpf(cpf: str) -> Optional['Morador']:
        try:
            db_manager = DatabaseManager()
            query = "SELECT * FROM usuario WHERE cpf = ? AND tipo_usuario = 'morador'"
            resultados = db_manager.executar_query(query, (cpf,))
            return Morador(**resultados[0]) if resultados else None
        except Exception:
            return None

    @staticmethod
    def buscar_por_id(morador_id: int) -> Morador | None:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE id = ? AND tipo_usuario = 'morador'"
        resultados = db_manager.executar_query(query, (morador_id,))
        return Morador(**resultados[0]) if resultados else None

    @staticmethod
    def buscar_nao_alocados() -> List[Morador]:
        db_manager = DatabaseManager()
        query = """
                SELECT u.* FROM usuario u
                WHERE u.tipo_usuario = 'morador' AND u.id NOT IN (SELECT morador_id FROM contrato WHERE status = 'ativo')
            """
        resultados = db_manager.executar_query(query)
        return [Morador(**r) for r in resultados]