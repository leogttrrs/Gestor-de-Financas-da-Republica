from .usuario import Usuario
from src.database.database_manager import DatabaseManager


class Administrador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, senhaCriptografada: str = None, id: int = None):
        super().__init__(cpf, nome, email, telefone, 'administrador', senhaCriptografada, id)

    @staticmethod
    def limpar_banco_dados() -> bool:
        try:
            db_manager = DatabaseManager()
            tabelas = [
                'alerta',
                'ocorrencia',
                'pagamento',
                'divida',
                'recorrencia',
                'contrato',
                'quarto',
                'republica',
                'usuario'
            ]

            db_manager.executar_comando("PRAGMA foreign_keys = OFF")
            for tabela in tabelas:
                check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
                if db_manager.executar_query(check_query, (tabela,)):
                    db_manager.executar_comando(f"DELETE FROM {tabela}")
                    db_manager.executar_comando(f"DELETE FROM sqlite_sequence WHERE name='{tabela}'")
            db_manager.executar_comando("PRAGMA foreign_keys = ON")

            return True

        except Exception as e:
            print(f"Erro crítico ao limpar banco de dados: {e}")
            return False