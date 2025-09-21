from models.usuario import Usuario


class Morador(Usuario):
    def __init__(self, id: int, cpf: str, nome: str, email: str, telefone: str, genero: str, senhaCriptografada: str = None):
        super().__init__(id, cpf, nome, email, telefone, genero, senhaCriptografada)