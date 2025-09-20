from model.usuario import Usuario

class Morador(Usuario):
    def __init__(self, id, nome, email, telefone, genero, cpf, senhaCriptografada):
        super().__init__(id, nome, email, telefone, genero, cpf, senhaCriptografada)
        self.contratos = []
        self.dividas = []
        self.ocorrencias = []
        self.alertas = []

    # Casos de uso
    def login(self, senha):
        return self.senhaCriptografada == senha

    def logout(self):
        return f"{self.nome} saiu do sistema."

    def redefinir_senha(self, nova_senha):
        self.senhaCriptografada = nova_senha
        return "Senha redefinida com sucesso!"

    def registrar_ocorrencia(self, ocorrencia):
        self.ocorrencias.append(ocorrencia)

    def visualizar_contatos_e_quartos(self):
        return [(c.quarto.numeroQuarto, c.quarto.tamanho) for c in self.contratos]

    def consultar_lista_moradores(self, moradores):
        return [m.nome for m in moradores]

    def visualizar_alertas(self):
        return self.alertas

    def consultar_historico_dividas(self):
        return [(d.nome, d.valorPendente, d.status) for d in self.dividas]

    def registrar_solicitacao_pagamento(self, divida_id):
        for d in self.dividas:
            if d.id == divida_id:
                return f"Solicitação de pagamento registrada para dívida {d.nome}"
        return "Dívida não encontrada."