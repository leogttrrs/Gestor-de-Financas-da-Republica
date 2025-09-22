# arquivo: src/controller/controlador_quarto.py

from .abstract_controlador import AbstractControlador
from src.views.tela_quarto import TelaQuarto
from src.views.tela_formulario_quarto import TelaFormularioQuarto
from src.models.Quarto import Quarto
from tkinter import messagebox


class ControladorQuarto(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_gerenciar = None

    def abre_tela(self, parent_view):
        self.tela_gerenciar = TelaQuarto(parent_view.content_frame, self._controlador_sistema)
        self._controlador_sistema.tela_atual = self.tela_gerenciar
        self.tela_gerenciar.mostrar()

    def abrir_tela_formulario(self, quarto_existente=None):
        # ANOTAÇÃO: Lógica de buscar moradores disponíveis foi removida
        root_window = self._controlador_sistema.tela_atual.frame.winfo_toplevel()
        TelaFormularioQuarto(root_window, self, quarto_existente)

    def salvar_quarto(self, dados: dict):
        # ANOTAÇÃO: Lógica de salvar e sincronizar moradores foi simplificada
        try:
            quarto = Quarto(
                id=dados.get("id"),
                numero_quarto=dados["numero_quarto"],
                tamanho=dados["tamanho"],
                republica_id=dados["republica_id"]
            )
            quarto.salvar()

            if self.tela_gerenciar:
                self.tela_gerenciar.atualizar_lista()
            return True, "Salvo com sucesso"
        except Exception as e:
            return False, str(e)

    def excluir_quarto(self, quarto_id: int):
        quarto = Quarto.buscar_por_id(quarto_id)
        if quarto:
            if quarto.possui_contratos_ativos():
                messagebox.showerror("Ação Proibida", "Não é possível excluir um quarto com contratos ativos.")
                return
            Quarto.deletar(quarto_id)
            if self.tela_gerenciar:
                self.tela_gerenciar.atualizar_lista()