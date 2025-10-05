from __future__ import annotations
from src.models.usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import Optional, List, Tuple
import sqlite3


class Morador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, genero: str, senhaCriptografada: str = None, id: int = None):
        super().__init__(cpf, nome, email, telefone, genero, senhaCriptografada, id)

    def salvar(self) -> Tuple[bool, str]:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                
                cursor.execute("SELECT id FROM usuario WHERE cpf = ?", (self.cpf,))
                if cursor.fetchone():
                    return False, "CPF já cadastrado no sistema"
                
                valido, mensagem = self.validar_dados()
                if not valido:
                    return False, mensagem
                
                if self.senhaCriptografada is None:
                    return False, "Senha é obrigatória"
                
                cursor.execute("""
                    INSERT INTO usuario (cpf, nome, email, telefone, genero, senhaCriptografada) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.cpf, self.nome, self.email, self.telefone, self.genero, self.senhaCriptografada))
                
                usuario_id = cursor.lastrowid
                
                cursor.execute("INSERT INTO morador (id) VALUES (?)", (usuario_id,))
                
                self.id = usuario_id
                return True, "Morador cadastrado com sucesso"
                
        except sqlite3.Error as e:
            return False, f"Erro ao salvar morador: {str(e)}"

    def atualizar(self) -> Tuple[bool, str]:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                
                cursor.execute("SELECT id FROM usuario WHERE cpf = ? AND id != ?", (self.cpf, self.id))
                if cursor.fetchone():
                    return False, "CPF já está sendo usado por outro usuário"
                
                valido, mensagem = self.validar_dados()
                if not valido:
                    return False, mensagem

                cursor.execute("""
                    UPDATE usuario 
                    SET nome = ?, email = ?, telefone = ?, genero = ?, senhaCriptografada = ? 
                    WHERE id = ?
                """, (self.nome, self.email, self.telefone, self.genero, self.senhaCriptografada, self.id))

                if cursor.rowcount > 0:
                    return True, "Perfil atualizado com sucesso"
                else:
                    return False, "Morador não encontrado para atualizar"

        except sqlite3.Error as e:
            return False, f"Erro ao atualizar morador: {str(e)}"

    # morador pode ser excluido apenas por adm?
    def excluir(self) -> Tuple[bool, str]:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                
                cursor.execute("DELETE FROM morador WHERE id = ?", (self.id,))
                cursor.execute("DELETE FROM usuario WHERE id = ?", (self.id,))
                
                if cursor.rowcount > 0:
                    return True, "Morador excluído com sucesso"
                else:
                    return False, "Morador não encontrado"
                    
        except sqlite3.Error as e:
            return False, f"Erro ao excluir morador: {str(e)}" 

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

    @staticmethod
    def buscar_por_id(morador_id: int) -> Morador | None:
        db_manager = DatabaseManager()
        query = "SELECT * FROM usuario WHERE id = ?"
        resultados = db_manager.executar_query(query, (morador_id,))
        return Morador(**resultados[0]) if resultados else None

    @staticmethod
    def buscar_nao_alocados() -> List[Morador]:
        db_manager = DatabaseManager()
        query = """
                SELECT u.* FROM usuario u
                JOIN morador m ON u.id = m.id
                WHERE u.id NOT IN (SELECT morador_id FROM contrato WHERE status = 'ativo')
            """
        resultados = db_manager.executar_query(query)
        return [Morador(**r) for r in resultados]