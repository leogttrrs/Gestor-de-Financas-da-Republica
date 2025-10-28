from abc import ABC, abstractmethod
from typing import Tuple, Optional
from ..utils.validador import Validador
from ..database.database_manager import DatabaseManager


class Usuario(ABC):
    @abstractmethod
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, tipo_usuario: str, senhaCriptografada: str = None, id: int = None, **kwargs):
        self.__id = None
        self.__cpf = None
        self.__nome = None
        self.__email = None
        self.__telefone = None
        self.__tipo_usuario = None
        self.__senhaCriptografada = None
        if isinstance(id, int) or id is None:
            self.__id = id
        if isinstance(cpf, str):
            self.__cpf = cpf
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(email, str):
            self.__email = email
        if isinstance(telefone, str):
            self.__telefone = telefone
        if isinstance(tipo_usuario, str) and tipo_usuario in ['administrador', 'morador']:
            self.__tipo_usuario = tipo_usuario
        if isinstance(senhaCriptografada, str) or senhaCriptografada is None:
            self.__senhaCriptografada = senhaCriptografada

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        if isinstance(cpf, str):
            self.__cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email):
        if isinstance(email, str):
            self.__email = email

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        if isinstance(telefone, str):
            self.__telefone = telefone

    @property
    def tipo_usuario(self) -> str:
        return self.__tipo_usuario

    @tipo_usuario.setter
    def tipo_usuario(self, tipo: str):
        if isinstance(tipo, str) and tipo in ['administrador', 'morador']:
            self.__tipo_usuario = tipo

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id):
        if isinstance(id, int) or id is None:
            self.__id = id

    @property
    def senhaCriptografada(self) -> str:
        return self.__senhaCriptografada

    @senhaCriptografada.setter
    def senhaCriptografada(self, senha_criptografada):
        if isinstance(senha_criptografada, str):
            self.__senhaCriptografada = senha_criptografada

    def validar_cpf(self, cpf: str) -> bool:
        resultado = Validador.validar_cpf(cpf)
        if isinstance(resultado, str) and ("inválido" in resultado or "Erro" in resultado):
            return False
        return True

    def hash_senha(self, senha: str) -> str:
        return Validador.hash_senha(senha)

    def verificar_senha(self, senha: str) -> bool:
        return self.hash_senha(senha) == self.__senhaCriptografada

    def validar_dados(self) -> Tuple[bool, str]:
        return Validador.validar_dados_usuario(
            self.__cpf,
            self.__nome,
            self.__email,
            self.__telefone
        )

    @staticmethod
    def salvar_usuario(usuario: 'Usuario') -> Tuple[bool, str]:
        try:
            valido, mensagem = usuario.validar_dados()
            if not valido:
                return False, mensagem
            
            with DatabaseManager() as db:
                cursor = db.cursor()
                
                cursor.execute("""
                    INSERT INTO usuario (cpf, nome, email, telefone, tipo_usuario, senhaCriptografada)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (usuario.cpf, usuario.nome, usuario.email, usuario.telefone,
                      usuario.tipo_usuario, usuario.senhaCriptografada))
                
                usuario_id = cursor.lastrowid
                usuario.id = usuario_id
                return True, f"{usuario.tipo_usuario} salvo com sucesso"
                
        except Exception as e:
            tipo = usuario.tipo_usuario if usuario and hasattr(usuario, 'tipo_usuario') else 'usuário'
            return False, f"Erro ao salvar {tipo}: {str(e)}"

    @staticmethod
    def atualizar_usuario(usuario: 'Usuario') -> Tuple[bool, str]:
        try:
            valido, mensagem = usuario.validar_dados()
            if not valido:
                return False, mensagem
            
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    UPDATE usuario 
                    SET cpf = ?, nome = ?, email = ?, telefone = ?, senhaCriptografada = ?
                    WHERE id = ?
                """, (usuario.cpf, usuario.nome, usuario.email, usuario.telefone,
                      usuario.senhaCriptografada, usuario.id))
                
                if cursor.rowcount > 0:
                    return True, f"{usuario.tipo_usuario} atualizado com sucesso"
                else:
                    return False, f"{usuario.tipo_usuario} não encontrado"
                    
        except Exception as e:
            tipo = usuario.tipo_usuario if usuario and hasattr(usuario, 'tipo_usuario') else 'usuário'
            return False, f"Erro ao atualizar {tipo}: {str(e)}"

    @staticmethod
    def excluir_usuario(cpf: str) -> Tuple[bool, str]:
        try:
            usuario = Usuario.buscar_por_cpf(cpf)
            if not usuario:
                return False, f"Usuário não encontrado"
            
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    DELETE FROM usuario WHERE id = ?
                """, (usuario.id,))
                
                if cursor.rowcount > 0:
                    return True, f"{usuario.tipo_usuario} excluído com sucesso"
                else:
                    return False, f"Erro ao excluir {usuario.tipo_usuario}"
                    
        except Exception as e:
            return False, f"Erro ao excluir usuário: {str(e)}"

    @staticmethod
    def buscar_por_cpf(cpf: str) -> Optional['Usuario']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT id, cpf, nome, email, telefone, tipo_usuario, senhaCriptografada
                    FROM usuario
                    WHERE cpf = ?
                """, (cpf,))
                row = cursor.fetchone()
                if row:
                    tipo = row['tipo_usuario']
                    if tipo == 'administrador':
                        from .Administrador import Administrador
                        return Administrador(
                            cpf=row['cpf'],
                            nome=row['nome'],
                            email=row['email'],
                            telefone=row['telefone'],
                            senhaCriptografada=row['senhaCriptografada'],
                            id=row['id']
                        )
                    elif tipo == 'morador':
                        from .Morador import Morador
                        return Morador(
                            cpf=row['cpf'],
                            nome=row['nome'],
                            email=row['email'],
                            telefone=row['telefone'],
                            senhaCriptografada=row['senhaCriptografada'],
                            id=row['id']
                        )
                return None
        except Exception as e:
            print(f"Erro ao buscar usuário por CPF: {e}")
            return None

    @staticmethod
    def alterar_senha(cpf: str, nova_senha: str) -> Tuple[bool, str]:
        try:
            usuario = Usuario.buscar_por_cpf(cpf)
            if not usuario:
                return False, "Usuário não encontrado"
            
            senha_criptografada = Validador.hash_senha(nova_senha)
            
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    UPDATE usuario 
                    SET senhaCriptografada = ? 
                    WHERE cpf = ?
                """, (senha_criptografada, cpf))
                
                if cursor.rowcount > 0:
                    return True, "Senha alterada com sucesso"
                else:
                    return False, "Erro ao alterar senha"
                    
        except Exception as e:
            return False, f"Erro ao alterar senha: {str(e)}"

    @staticmethod
    def buscar_por_id(id: int, tipo_usuario: str = None) -> Optional['Usuario']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                if tipo_usuario:
                    cursor.execute("""
                        SELECT id, cpf, nome, email, telefone, tipo_usuario, senhaCriptografada
                        FROM usuario
                        WHERE id = ? AND tipo_usuario = ?
                    """, (id, tipo_usuario))
                else:
                    cursor.execute("""
                        SELECT id, cpf, nome, email, telefone, tipo_usuario, senhaCriptografada
                        FROM usuario
                        WHERE id = ?
                    """, (id,))
                
                row = cursor.fetchone()
                if row:
                    if row['tipo_usuario'] == 'administrador':
                        from .Administrador import Administrador
                        return Administrador(row['cpf'], row['nome'], row['email'], row['telefone'], row['senhaCriptografada'], row['id'])
                    elif row['tipo_usuario'] == 'morador':
                        from .Morador import Morador
                        return Morador(row['cpf'], row['nome'], row['email'], row['telefone'], row['senhaCriptografada'], row['id'])
                return None
                
        except Exception:
            return None

    @staticmethod
    def existe_algum(tipo_usuario: str) -> bool:
        try:
            db_manager = DatabaseManager()
            resultado = db_manager.executar_query("SELECT 1 FROM usuario WHERE tipo_usuario = ? LIMIT 1", (tipo_usuario,))
            return len(resultado) > 0
        except Exception:
            return False

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'tipo_usuario': self.tipo_usuario,
            'senhaCriptografada': self.senhaCriptografada
        }