from src.models.usuario import Usuario
from src.database.database_manager import DatabaseManager
from typing import Optional, Tuple


class Administrador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, senhaCriptografada: str = None, id: int = None):
        super().__init__(cpf, nome, email, telefone, 'administrador', senhaCriptografada, id)

    def salvar(self) -> Tuple[bool, str]:
        return Usuario.salvar_usuario(self)

    def atualizar(self) -> Tuple[bool, str]:
        return Usuario.atualizar_usuario(self)

    def excluir(self) -> Tuple[bool, str]:
        return Usuario.excluir_usuario(self.cpf)

    @staticmethod
    def existe_algum() -> bool:
        try:
            db_manager = DatabaseManager()
            resultado = db_manager.executar_query("SELECT 1 FROM usuario WHERE tipo_usuario = 'administrador' LIMIT 1")
            return len(resultado) > 0
        except Exception as e:
            return False

    @staticmethod
    def buscar_por_id(id: int) -> Optional['Administrador']:
        try:
            with DatabaseManager() as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT id, cpf, nome, email, telefone, tipo_usuario, senhaCriptografada
                    FROM usuario
                    WHERE id = ? AND tipo_usuario = 'administrador'
                """, (id,))
                row = cursor.fetchone()
                if row:
                    admin = Administrador(row['cpf'], row['nome'], row['email'], row['telefone'], row['senhaCriptografada'], row['id'])
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
            'tipo_usuario': self.tipo_usuario,
            'senhaCriptografada': self.senhaCriptografada
        }
