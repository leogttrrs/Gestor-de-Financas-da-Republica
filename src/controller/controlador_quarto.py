import sqlite3
from .abstract_controlador import AbstractControlador
from src.views.tela_quarto import TelaQuarto
from src.views.tela_formulario_quarto import TelaFormularioQuarto
from src.models.Quarto import Quarto
from tkinter import messagebox
from src.models.Republica import Republica


class ControladorQuarto(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_gerenciar = None

    def abre_tela(self, parent_view):
        self.tela_gerenciar = TelaQuarto(parent_view.content_frame, self._controlador_sistema)
        self._controlador_sistema.tela_atual = self.tela_gerenciar
        self.tela_gerenciar.mostrar()

    def abrir_tela_formulario(self, quarto_existente=None):
        root_window = self._controlador_sistema.tela_atual.frame.winfo_toplevel()
        TelaFormularioQuarto(root_window, self, quarto_existente)

    def salvar_quarto(self, dados: dict):
        try:
            admin_logado = self._controlador_sistema.usuario_logado
            if not admin_logado:
                return False, "Nenhum administrador está logado."

            republica_atual = Republica.buscar_por_admin_id(admin_logado.id)
            if not republica_atual:
                return False, "Nenhuma república encontrada para o administrador atual."

            dados["republica_id"] = republica_atual.id

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

        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                num_quarto = dados.get('numero_quarto', '')
                return False, f"Já existe um quarto com o número {num_quarto}."
            else:
                return False, f"Erro de integridade no banco de dados: {e}"
        except Exception as e:
            return False, f"Um erro inesperado ocorreu: {e}"

    def excluir_quarto(self, quarto_id: int):
        quarto = Quarto.buscar_por_id(quarto_id)
        if quarto:
            if quarto.possui_contratos_ativos():
                messagebox.showerror("Ação Proibida", "Não é possível excluir um quarto com contratos ativos.")
                return
            Quarto.deletar(quarto_id)
            if self.tela_gerenciar:
                self.tela_gerenciar.atualizar_lista()