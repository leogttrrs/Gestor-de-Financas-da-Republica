class Usuario:
    #cria os atributos da classe Usuario
    def __init__(self, nome, email, telefone, genero, cpf, senhaCripografada):
        self.id = None  # ID será atribuído ao salvar no banco de dados
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.genero = genero
        self.cpf = cpf
        self.senhaCripografada = senhaCripografada

    def get_id(self):
        return self.id
    def set_id(self, id):
        self.id = id
    
    def get_nome(self):
        return self.nome
    def set_nome(self, nome):
        self.nome = nome

    def get_email(self):    
        return self.email
    def set_email(self, email):
        self.email = email
    
    def get_telefone(self):
        return self.telefone   
    def set_telefone(self, telefone):
        self.telefone = telefone
    
    def get_genero(self):
        return self.genero
    def set_genero(self, genero):
        self.genero = genero

    def get_cpf(self):
        return self.cpf
    def set_cpf(self, cpf):
        self.cpf = cpf
   
    def get_senhaCripografada(self):
        return self.senhaCripografada
    def set_senhaCripografada(self, senhaCripografada):
        self.senhaCripografada = senhaCripografada