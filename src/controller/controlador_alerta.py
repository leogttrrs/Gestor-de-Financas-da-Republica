from .abstract_controlador import AbstractControlador
from src.models.Alerta import Alerta
from src.models.Administrador import Administrador
from src.views.tela_alerta import TelaAlerta
from tkinter import messagebox


class ControladorAlerta(AbstractControlador):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.tela_alertas = None

    def abre_tela(self, parent_view=None):
        usuario = self._controlador_sistema.usuario_logado
        eh_admin = isinstance(usuario, Administrador)

        self.tela_alertas = TelaAlerta(
            parent_view.content_frame,
            self,
            eh_admin=eh_admin
        )

        self.atualizar_lista_alertas()

        self._controlador_sistema.tela_atual = self.tela_alertas
        self.tela_alertas.mostrar()

    def atualizar_lista_alertas(self):
        lista = Alerta.buscar_todos()
        if self.tela_alertas:
            self.tela_alertas.atualizar_lista(lista)

    def salvar_alerta(self, descricao):
        try:
            novo = Alerta(descricao=descricao)
            novo.salvar()
            self.atualizar_lista_alertas()
            messagebox.showinfo("Sucesso", "Alerta publicado com sucesso!")
        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar alerta: {e}")

    def excluir_alerta(self, alerta_id):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este alerta?"):
            if Alerta.excluir(alerta_id):
                self.atualizar_lista_alertas()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir o alerta.")