from model.morador import Morador

class MoradorController:
    def __init__(self, view):
        self.view = view
        self.moradores = []
        self.morador_logado = None  # para simular login

    
    # -------- Métodos chamados pelos botões --------
    def gerenciar_ocorrencias(self):
        if self.morador_logado:
            self.morador_logado.registrar_ocorrencia("Ocorrência exemplo")
            self.view.exibir_mensagem("Ocorrência registrada com sucesso!")

    def visualizar_contatos_e_quartos(self):
        if self.morador_logado:
            lista = self.morador_logado.visualizar_contatos_e_quartos()
            self.view.exibir_lista(lista, titulo="Contatos e Quartos")

    def consultar_lista_moradores(self):
        lista = [m.nome for m in self.moradores]
        self.view.exibir_lista(lista, titulo="Lista de Moradores")

    def visualizar_alertas(self):
        if self.morador_logado:
            lista = self.morador_logado.visualizar_alertas()
            if lista:
                self.view.exibir_lista(lista, titulo="Alertas")
            else:
                self.view.exibir_mensagem("Nenhum alerta encontrado.")

    def consultar_historico_dividas(self):
        if self.morador_logado:
            lista = self.morador_logado.consultar_historico_dividas()
            self.view.exibir_lista(lista, titulo="Histórico de Dívidas")

    def registrar_solicitacao_pagamento(self):
        if self.morador_logado and self.morador_logado.dividas:
            d = self.morador_logado.dividas[0]
            msg = self.morador_logado.registrar_solicitacao_pagamento(d.id)
            self.view.exibir_mensagem(msg)
        else:
            self.view.exibir_mensagem("Nenhuma dívida encontrada.")
