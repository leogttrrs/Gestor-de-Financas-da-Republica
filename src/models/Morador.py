from src.models.usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import Optional


class Morador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, genero: str, senhaCriptografada: str = None, id: int = None):
        super().__init__(cpf, nome, email, telefone, genero, senhaCriptografada, id)

    def salvar(self):
        pass

    def atualizar(self):
        pass

    def excluir(self):
        pass

    @staticmethod
    def buscar_por_cpf(cpf: str) -> Optional['Morador']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT u.id, u.cpf, u.nome, u.email, u.telefone, u.genero, u.senhaCriptografada 
                    FROM usuario u
                    INNER JOIN morador m ON u.id = m.id 
                    WHERE u.cpf = ?
                """, (cpf,))
                
                row = cursor.fetchone()
                if row:
                    morador = Morador(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
                    return morador
                return None
                
        except Exception:
            return None