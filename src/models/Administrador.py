from src.models.usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import Optional, List, Tuple
import sqlite3


class Administrador(Usuario):
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
                
                cursor.execute("INSERT INTO administrador (id) VALUES (?)", (usuario_id,))
                
                self.id = usuario_id
                return True, "Administrador cadastrado com sucesso"
                
        except sqlite3.Error as e:
            return False, f"Erro ao salvar administrador: {str(e)}"

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
                
                if self.__senha and len(self.__senha) < 6:
                    return False, "Senha deve ter pelo menos 6 caracteres"
                
                if self.__senha:
                    senha_hash = self.hash_senha(self.__senha)
                    self.senhaCriptografada = senha_hash
                    cursor.execute("""
                        UPDATE usuario 
                        SET nome = ?, email = ?, telefone = ?, genero = ?, senhaCriptografada = ? 
                        WHERE id = ?
                    """, (self.nome, self.email, self.telefone, self.genero, senha_hash, self.id))
                else:
                    cursor.execute("""
                        UPDATE usuario 
                        SET nome = ?, email = ?, telefone = ?, genero = ? 
                        WHERE id = ?
                    """, (self.nome, self.email, self.telefone, self.genero, self.id))
                
                if cursor.rowcount > 0:
                    return True, "Perfil atualizado com sucesso"
                else:
                    return False, "Administrador não encontrado"
                    
        except sqlite3.Error as e:
            return False, f"Erro ao atualizar administrador: {str(e)}"

    def excluir(self) -> Tuple[bool, str]:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                
                cursor.execute("DELETE FROM usuarios WHERE id = ? AND tipo_usuario = 'administrador'", (self.id,))
                
                if cursor.rowcount > 0:
                    return True, "Administrador excluído com sucesso"
                else:
                    return False, "Administrador não encontrado"
                    
        except sqlite3.Error as e:
            return False, f"Erro ao excluir administrador: {str(e)}"

    @staticmethod
    def buscar_por_id(id: int) -> Optional['Administrador']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT id, cpf, nome, email, telefone, genero, senha_hash 
                    FROM usuarios 
                    WHERE id = ? AND tipo_usuario = 'administrador'
                """, (id,))
                
                row = cursor.fetchone()
                if row:
                    admin = Administrador(row[0], row[1], row[2], row[3], row[4], row[5], "", row[6])
                    return admin
                return None
                
        except Exception:
            return None

    @staticmethod
    def buscar_por_cpf(cpf: str) -> Optional['Administrador']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT u.id, u.cpf, u.nome, u.email, u.telefone, u.genero, u.senhaCriptografada 
                    FROM usuario u
                    INNER JOIN administrador a ON u.id = a.id 
                    WHERE u.cpf = ?
                """, (cpf,))
                
                row = cursor.fetchone()
                if row:
                    admin = Administrador(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
                    return admin
                return None
                
        except Exception:
            return None

    @staticmethod
    def listar_todos() -> List['Administrador']:
        administradores = []
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT u.id, u.cpf, u.nome, u.email, u.telefone, u.genero, u.senhaCriptografada 
                    FROM usuario u
                    INNER JOIN administrador a ON u.id = a.id
                    ORDER BY u.nome
                """)
                
                for row in cursor.fetchall():
                    admin = Administrador(
                        cpf=row[1], 
                        nome=row[2], 
                        email=row[3], 
                        telefone=row[4], 
                        genero=row[5], 
                        senhaCriptografada=row[6],
                        id=row[0]
                    )
                    administradores.append(admin)
                    
        except Exception as e:
            print(f"Erro ao listar administradores: {e}")
        
        return administradores

    @staticmethod
    def autenticar(cpf: str, senha: str) -> Optional['Administrador']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                
                admin = Administrador.buscar_por_cpf(cpf)
                if not admin:
                    return None
                
                senha_hash = admin.hash_senha(senha)
                cursor.execute("""
                    SELECT id FROM usuarios 
                    WHERE cpf = ? AND senha_hash = ? AND tipo_usuario = 'administrador'
                """, (cpf, senha_hash))
                
                if cursor.fetchone():
                    return admin
                return None
                
        except Exception:
            return None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'genero': self.genero,
            'senha': self.senha,
            'senhaCriptografada': self.senhaCriptografada
        }
