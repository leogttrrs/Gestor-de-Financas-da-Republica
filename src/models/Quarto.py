class Quarto:
    def __init__(self, id, numero, tamanho, capacidade, status):
        self.id = id
        self.numero = numero
        self.tamanho = tamanho
        self.capacidade = capacidade
        self.status = status

        self.moradores = []

    def __repr__(self):
        return f"Quarto(ID: {self.id}, Nº: {self.numero}, Status: {self.status})"