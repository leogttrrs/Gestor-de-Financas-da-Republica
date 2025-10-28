from src.models.usuario import Usuario


class Administrador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, telefone: str, senhaCriptografada: str = None, id: int = None):
        super().__init__(cpf, nome, email, telefone, 'administrador', senhaCriptografada, id)

