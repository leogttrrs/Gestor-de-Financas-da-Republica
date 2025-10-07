from __future__ import annotations
from src.models.usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import Optional, List


class Morador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, senhaCriptografada: str = None, id: int = None):
        super().__init__(cpf, nome, email, telefone, 'morador', senhaCriptografada, id)

    def salvar(self):
        return Usuario.salvar_usuario(self)

    def atualizar(self):
        return Usuario.atualizar_usuario(self)

    def excluir(self):
        return Usuario.excluir_usuario(self.cpf)

    @staticmethod
    def buscar_por_cpf(cpf: str) -> Optional['Morador']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT id, cpf, nome, email, telefone, tipo_usuario, senhaCriptografada
                    FROM usuario
                    WHERE cpf = ? AND tipo_usuario = 'morador'
                """, (cpf,))
                row = cursor.fetchone()
                if row:
                    morador = Morador(row['cpf'], row['nome'], row['email'], row['telefone'], row['senhaCriptografada'], row['id'])
                    return morador
                return None
        except Exception:
            return None

    @staticmethod
    def buscar_por_id(morador_id: int) -> Morador | None:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE id = ? AND tipo_usuario = 'morador'"
        resultados = db_manager.executar_query(query, (morador_id,))
        return Morador(resultados[0]['cpf'], resultados[0]['nome'], resultados[0]['email'], resultados[0]['telefone'], resultados[0]['senhaCriptografada'], resultados[0]['id']) if resultados else None

    @staticmethod
    def buscar_nao_alocados() -> List[Morador]:
        db_manager = DatabaseManager()
        query = """
                SELECT u.* FROM usuario u
                WHERE u.tipo_usuario = 'morador' AND u.id NOT IN (SELECT morador_id FROM contrato WHERE status = 'ativo')
            """
        resultados = db_manager.executar_query(query)
        return [Morador(r['cpf'], r['nome'], r['email'], r['telefone'], r['senhaCriptografada'], r['id']) for r in resultados]