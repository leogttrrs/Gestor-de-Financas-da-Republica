import tkinter as tk
from tkinter import ttk
from .tela_formulario_morador import TelaFormularioMorador
from .aplicacao_spa import ComponenteBase


class TelaMoradores(ComponenteBase):
    def __init__(self, container, controlador_sistema, controlador_morador):
        super().__init__(container, controlador_sistema)
        self.controlador_morador = controlador_morador
        self.lista_moradores = []

        self.eh_admin = (self.controlador_sistema.usuario_logado.tipo_usuario == 'administrador')

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
        style.configure("Btn.Editar.TButton", background="#ffc107", foreground="black", borderwidth=0)
        style.map("Btn.Editar.TButton", background=[('active', '#e0a800')])
        style.configure("Btn.Excluir.TButton", background="#dc3545", foreground="white", borderwidth=0)
        style.map("Btn.Excluir.TButton", background=[('active', '#c82333')])

    def _criar_interface(self):
        self.criar_frame()
        self.frame.configure(style="Moradores.TFrame")

        header = ttk.Frame(self.frame, style="Moradores.TFrame")
        header.pack(fill="x", pady=(0, 10))

        titulo = ttk.Label(header, text="Lista de Moradores", font=("Arial", 20, "bold"),
                           style="Moradores.TLabel")
        titulo.pack(side="left")

        if self.eh_admin:
            ttk.Button(
                header,
                text="+ Cadastrar Morador",
                style="Btn.Abrir.TButton",
                command=self.abrir_modal_morador
            ).pack(side="right")

        canvas_container = ttk.Frame(self.frame, style="Moradores.TFrame")
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)

        self.container_lista = ttk.Frame(self.canvas, style="Moradores.TFrame")

        self.container_lista.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.container_lista, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.container_lista.winfo_children():
            widget.destroy()

        self.lista_moradores = self.controlador_morador.listar_todos_detalhado()

        header = ttk.Frame(self.container_lista, style="Row.TFrame")
        header.pack(fill="x", pady=5)

        ttk.Label(header, text="Nome", width=25, font=('Arial', 10, 'bold'), style="Row.TLabel").pack(side="left",
                                                                                                      padx=5)
        ttk.Label(header, text="Quarto", width=8, font=('Arial', 10, 'bold'), style="Row.TLabel").pack(side="left",
                                                                                                       padx=5)
        ttk.Label(header, text="Email", width=25, font=('Arial', 10, 'bold'), style="Row.TLabel").pack(side="left",
                                                                                                       padx=5)
        ttk.Label(header, text="Telefone", width=15, font=('Arial', 10, 'bold'), style="Row.TLabel").pack(side="left",
                                                                                                          padx=5)
        if self.eh_admin:
            ttk.Label(header, text="Ações", width=15, font=('Arial', 10, 'bold'), style="Row.TLabel").pack(side="right",
                                                                                                           padx=20)

        if not self.lista_moradores:
            vazio = ttk.Label(self.container_lista, text="Nenhum morador cadastrado.", style="Row.TLabel",
                              foreground="#888")
            vazio.pack(pady=20)
            return

        for morador in self.lista_moradores:
            linha = ttk.Frame(self.container_lista, style="Row.TFrame")
            linha.pack(fill="x", pady=5)

            ttk.Label(linha, text=morador['nome'], width=25, style="Row.TLabel").pack(side="left", padx=5)
            ttk.Label(linha, text=morador['quarto_numero'], width=8, style="Row.TLabel").pack(side="left", padx=5)
            ttk.Label(linha, text=morador['email'], width=25, style="Row.TLabel").pack(side="left", padx=5)
            ttk.Label(linha, text=morador['telefone'], width=15, style="Row.TLabel").pack(side="left", padx=5)

            if self.eh_admin:
                acoes_frame = ttk.Frame(linha, style="Row.TFrame")
                acoes_frame.pack(side="right", padx=10)

                btn_excluir = ttk.Button(acoes_frame, text="Excluir", style="Btn.Excluir.TButton", width=8,
                                         command=lambda id=morador['id']: self.controlador_morador.excluir_morador(id))
                btn_excluir.pack(side="right")

                btn_editar = ttk.Button(acoes_frame, text="Editar", style="Btn.Editar.TButton", width=8,
                                        command=lambda m=morador: self.abrir_modal_edicao(m))
                btn_editar.pack(side="right", padx=5)

    def abrir_modal_edicao(self, dados_morador):
        modal = tk.Toplevel(self.frame)
        modal.title(f"Editar {dados_morador['nome']}")
        modal.geometry("400x350")
        modal.configure(bg="white")

        ttk.Label(modal, text="CPF (Não editável)", background="white").pack(anchor="w", padx=20, pady=(20, 0))
        entry_cpf = ttk.Entry(modal)
        entry_cpf.insert(0, dados_morador['cpf'])
        entry_cpf.configure(state="readonly")
        entry_cpf.pack(fill="x", padx=20, pady=(5, 10))

        ttk.Label(modal, text="Nome", background="white").pack(anchor="w", padx=20)
        entry_nome = ttk.Entry(modal)
        entry_nome.insert(0, dados_morador['nome'])
        entry_nome.pack(fill="x", padx=20, pady=(5, 10))

        ttk.Label(modal, text="Email", background="white").pack(anchor="w", padx=20)
        entry_email = ttk.Entry(modal)
        entry_email.insert(0, dados_morador['email'])
        entry_email.pack(fill="x", padx=20, pady=(5, 10))

        ttk.Label(modal, text="Telefone", background="white").pack(anchor="w", padx=20)
        entry_tel = ttk.Entry(modal)
        entry_tel.insert(0, dados_morador['telefone'])
        entry_tel.pack(fill="x", padx=20, pady=(5, 10))

        def salvar():
            novos = {
                'nome': entry_nome.get(),
                'email': entry_email.get(),
                'telefone': entry_tel.get()
            }
            if self.controlador_morador.atualizar_morador_existente(dados_morador['id'], novos):
                modal.destroy()
                self.atualizar_lista()

        ttk.Button(modal, text="Salvar Alterações", command=salvar, style="Btn.Abrir.TButton").pack(pady=20)

    def abrir_modal_morador(self):
        TelaFormularioMorador(
            parent=self.frame,
            controlador_morador=self.controlador_morador,
            callback_cadastrar=lambda *args: self.atualizar_lista()
        )