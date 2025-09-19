import classe_usuario

class Administrador(classe_usuario.Usuario):  # herda de Usuario
    def __init__(self, nome, email, telefone, genero, cpf, senhaCripografada):
        # chama o construtor da classe pai
        super().__init__(nome, email, telefone, genero, cpf, senhaCripografada)