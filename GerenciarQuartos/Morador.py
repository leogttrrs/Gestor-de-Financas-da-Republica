class Morador:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __repr__(self):
        return f"Morador(ID: {self.id}, Nome: {self.nome})"