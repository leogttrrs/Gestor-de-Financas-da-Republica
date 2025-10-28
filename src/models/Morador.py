from __future__ import annotations
from .usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import List

class Morador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, senhaCriptografada: str = None, id: int = None, **kwargs):
        super().__init__(cpf, nome, email, telefone, 'morador', senhaCriptografada, id)

    @staticmethod
    def buscar_todos() -> List[Morador]:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE tipo_usuario = 'morador' ORDER BY nome"
        resultados = db_manager.executar_query(query)
        return [Morador(**r) for r in resultados]

    @staticmethod
    def buscar_nao_alocados() -> List[Morador]:
        db_manager = DatabaseManager()
        query = """
            SELECT u.* FROM usuario u
            WHERE u.tipo_usuario = 'morador' 
            AND u.id NOT IN (
                SELECT c.morador_id 
                FROM contrato c 
                WHERE c.status IN ('ativo', 'agendado')
            )
        """
        resultados = db_manager.executar_query(query)
        return [Morador(**r) for r in resultados]
    
    @staticmethod
    def tem_contrato_ativo(morador_id: int) -> bool:
        db_manager = DatabaseManager()
        query = """
            SELECT 1 FROM contrato c 
            INNER JOIN usuario u ON c.morador_id = u.id 
            WHERE c.morador_id = ? AND c.status = 'ativo' 
        """
        resultados = db_manager.executar_query(query, (morador_id,))
        return len(resultados) > 0
    
    @staticmethod
    def tem_contrato_agendado(morador_id: int) -> bool:
        db_manager = DatabaseManager()
        query = """
            SELECT 1 FROM contrato c 
            INNER JOIN usuario u ON c.morador_id = u.id 
            WHERE c.morador_id = ? AND c.status = 'agendado' 
        """
        resultados = db_manager.executar_query(query, (morador_id,))
        return len(resultados) > 0
