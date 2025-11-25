import tkinter as tk
from tkinter import ttk

from views.tela_formulario_morador import TelaFormularioMorador
from .aplicacao_spa import ComponenteBase


class TelaMoradores(ComponenteBase):
    def __init__(self, container, controlador_sistema, controlador_morador):
        super().__init__(container, controlador_sistema)
        self.controlador_morador = controlador_morador
        self.lista_moradores = []

        self.container_lista = None
        self._configurar_estilos()
        self._criar_interface()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Moradores.TFrame", background="white")
        style.configure("Moradores.TLabel", background="white")
        style.configure("Row.TFrame", background="white")
        style.configure("Row.TLabel", font=('Arial', 10), background="white")
        style.configure("Btn.Abrir.TButton", background="#007bff", foreground="white", borderwidth=0)
        style.map("Btn.Abrir.TButton", background=[('active', '#0069d9')])

    def _criar_interface(self):
        self.criar_frame()
        self.frame.configure(style="Moradores.TFrame")

        header = ttk.Frame(self.frame, style="Moradores.TFrame")
        header.pack(fill="x", pady=(0, 10))

        titulo = ttk.Label(header, text="Lista de Moradores", font=("Arial", 20, "bold"),
                           style="Moradores.TLabel")
        titulo.pack(side="left")

        # Botão cadastrar — fica sempre no topo (somente admins)
        if self.controlador_sistema.usuario_logado.tipo_usuario == 'administrador':
            ttk.Button(
                header,
                text="Cadastrar Morador",
                style="Btn.Abrir.TButton",
                command=self.abrir_modal_morador
            ).pack(side="right")

        # Container da lista
        self.container_lista = ttk.Frame(self.frame, style="Moradores.TFrame")
        self.container_lista.pack(fill="both", expand=True)

        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpa container
        for widget in self.container_lista.winfo_children():
            widget.destroy()

        self.lista_moradores = self.controlador_morador.listar_moradores_alocados()

        # Cabeçalho
        header = ttk.Frame(self.container_lista, style="Row.TFrame")
        header.pack(fill="x", pady=5)

        ttk.Label(header, text="Nome", width=25, style="Row.TLabel").pack(side="left")
        ttk.Label(header, text="Quarto", width=10, style="Row.TLabel").pack(side="left")
        ttk.Label(header, text="Email", width=25, style="Row.TLabel").pack(side="left")
        ttk.Label(header, text="Telefone", width=15, style="Row.TLabel").pack(side="left")

        # Linhas
        if not self.lista_moradores:
            vazio = ttk.Label(
                self.container_lista,
                text="Nenhum morador alocado.",
                style="Row.TLabel"
            )
            vazio.pack(pady=10)
            return

        for morador in self.lista_moradores:
            linha = ttk.Frame(self.container_lista, style="Row.TFrame")
            linha.pack(fill="x", pady=2)

            ttk.Label(linha, text=morador['morador_nome'], width=25, style="Row.TLabel").pack(side="left")
            ttk.Label(linha, text=morador['quarto_numero'], width=10, style="Row.TLabel").pack(side="left")
            ttk.Label(linha, text=morador['email'], width=25, style="Row.TLabel").pack(side="left")
            ttk.Label(linha, text=morador['telefone'], width=15, style="Row.TLabel").pack(side="left")

    def abrir_modal_morador(self):
        TelaFormularioMorador(
            parent=self.frame,
            controlador_morador=self.controlador_morador,  
            callback_cadastrar=None  # ou algum método, se quiser atualizar a lista depois
        )
