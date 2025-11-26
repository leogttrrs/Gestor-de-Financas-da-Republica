from __future__ import annotations

from utils.validador import Validador
from .usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import List

class Morador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, senhaCriptografada: str = None, id: int = None,
                 **kwargs):
        super().__init__(cpf, nome, email, telefone, 'morador', senhaCriptografada, id)

    @staticmethod
    def buscar_todos() -> List[Morador]:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE tipo_usuario = 'morador' ORDER BY nome"
        resultados = db_manager.executar_query(query)
        return [Morador(**r) for r in resultados]

    @staticmethod
    def buscar_com_contrato_ativo() -> List[Morador]:
        db_manager = DatabaseManager()
        query = """
            SELECT DISTINCT u.* FROM usuario u
            INNER JOIN contrato c ON u.id = c.morador_id
            WHERE u.tipo_usuario = 'morador' 
            AND c.status = 'ativo'
            ORDER BY u.nome
        """
        resultados = db_manager.executar_query(query)

        if not resultados:
            return []

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
    
    @staticmethod
    def buscar_por_cpf(cpf: str) -> Morador | None:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE cpf = ? AND tipo_usuario = 'morador'"
        resultados = db_manager.executar_query(query, (cpf,))
        return Morador(**resultados[0]) if resultados else None
    
    @staticmethod
    def buscar_por_id(morador_id: int) -> Morador | None:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE id = ? AND tipo_usuario = 'morador'"
        resultados = db_manager.executar_query(query, (morador_id,))
        return Morador(**resultados[0]) if resultados else None
    
    @staticmethod
    def excluir(morador_id: int) -> bool:
        db_manager = DatabaseManager()
        query = "DELETE FROM usuario WHERE id = ? AND tipo_usuario = 'morador'"
        linhas_afetadas = db_manager.executar_comando(query, (morador_id,))
        return linhas_afetadas > 0
    
    def salvar(self) -> Morador:
        # 1 — valida
        valido, mensagem = self.validar_dados()
        if not valido:
            raise ValueError(f"Erro de validação ao salvar morador: {mensagem}")

        # 2 — garante que senha tenha hash
        if self.senhaCriptografada and not Validador.eh_hash(self.senhaCriptografada):
            self.senhaCriptografada = Validador.hash_senha(self.senhaCriptografada)

        # 3 — delega tudo ao Usuario
        if self.id is None:
            sucesso, mensagem = Usuario.salvar_usuario(self)
        else:
            sucesso, mensagem = Usuario.atualizar_usuario(self)

        if not sucesso:
            raise RuntimeError(mensagem)

        return self

        

        