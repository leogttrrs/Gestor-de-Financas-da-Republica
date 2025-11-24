import tkinter as tk
from tkinter import ttk
from .aplicacao_spa import ComponenteBase


class TelaDividas(ComponenteBase):
    def __init__(self, container, controlador_sistema, moradores):
        super().__init__(container, controlador_sistema)
        self.frame_lista_dividas = None
        self.frame_avaliar_pagamentos = None
        self.frame_historico = None
        self.container_lista = None
        self.moradores = moradores

        self.ordenacao_var = tk.StringVar(value="Data de Vencimento")
        self.mostrar_quitadas_var = tk.IntVar(value=0)

        self._configurar_estilos()
        self._criar_interface()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Dividas.TFrame", background="white")
        style.configure("Dividas.TLabel", background="white")
        style.configure("Dividas.TNotebook", background="white")
        style.configure("TNotebook.Tab", background="#f0f0f0", padding=[10, 5], font=('Arial', 10))
        style.map("TNotebook.Tab", background=[("selected", "white")])
        style.configure("Status.Quitada.TLabel", foreground="#28a745", background="white", font=('Arial', 9, 'bold'))
        style.configure("Status.Pendente.TLabel", foreground="#6c757d", background="white", font=('Arial', 9, 'bold'))
        style.configure("Status.Vencida.TLabel", foreground="#dc3545", background="white", font=('Arial', 9, 'bold'))
        style.configure("Status.Confirmado.TLabel", foreground="#28a745", background="white", font=('Arial', 9, 'bold'))
        style.configure("Status.Cancelado.TLabel", foreground="#dc3545", background="white", font=('Arial', 9, 'bold'))
        style.configure("Editar.TButton", foreground="white", background="#007bff", borderwidth=0, font=('Arial', 9))
        style.configure("Excluir.TButton", foreground="white", background="#dc3545", borderwidth=0, font=('Arial', 9))
        style.configure("Salvar.TButton", foreground="white", background="#28a745", borderwidth=0, font=('Arial', 9))
        style.configure("Solicitado.TButton", foreground="black", background="#ffc107", borderwidth=0, font=('Arial', 9))

        style.map("Editar.TButton", background=[('active', '#0069d9')])
        style.map("Excluir.TButton", background=[('active', '#c82333')])
        style.map("Salvar.TButton", background=[('active', '#218838')])
        style.map("Solicitado.TButton", background=[('active', '#e0a800')])

    def _criar_interface(self):
        self.criar_frame()
        self.frame.configure(style="Dividas.TFrame")

        header_frame = ttk.Frame(self.frame, style="Dividas.TFrame")
        header_frame.pack(fill="x", pady=(0, 15))
        title_label = ttk.Label(header_frame, text="Gerenciamento de Dívidas", font=("Arial", 20, "bold"),
                                style="Dividas.TLabel")
        title_label.pack(side="left")

        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill="both", expand=True)

        self.frame_lista_dividas = ttk.Frame(notebook, padding=10, style="Dividas.TFrame")
        self.frame_avaliar_pagamentos = ttk.Frame(notebook, padding=10, style="Dividas.TFrame")
        self.frame_historico = ttk.Frame(notebook, padding=10, style="Dividas.TFrame")

        notebook.add(self.frame_lista_dividas, text="  Dívidas Atuais  ")

        usuario_logado = self.controlador_sistema.usuario_logado
        if usuario_logado and usuario_logado.tipo_usuario == 'morador':
            notebook.add(self.frame_avaliar_pagamentos, text="  Acompanhar Pagamentos  ")
        else:
            notebook.add(self.frame_avaliar_pagamentos, text="  Avaliar Pagamentos  ")

        notebook.add(self.frame_historico, text="  Histórico  ")

        self._popular_aba_lista_dividas()
        self._carregar_conteudo_abas()

    def _carregar_conteudo_abas(self):
        usuario_logado = self.controlador_sistema.usuario_logado
        self.controlador_sistema.controlador_divida.carregar_pagamentos_pendentes(
            self.frame_avaliar_pagamentos, usuario_logado
        )
        self.controlador_sistema.controlador_divida.carregar_historico(
            self.frame_historico, usuario_logado
        )

    def _popular_aba_lista_dividas(self):
        controles_frame = ttk.Frame(self.frame_lista_dividas, style="Dividas.TFrame")
        controles_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(controles_frame, text="Ordenar por:", style="Dividas.TLabel").pack(side="left", padx=(0, 5))
        combo_ordenacao = ttk.Combobox(controles_frame, textvariable=self.ordenacao_var,
                                       values=["Data de Vencimento", "Morador", "Valor"], state="readonly", width=20)
        combo_ordenacao.pack(side="left", padx=5)
        combo_ordenacao.bind("<<ComboboxSelected>>", self.atualizar_lista)

        check_quitadas = ttk.Checkbutton(controles_frame, text="Mostrar dívidas quitadas?",
                                         variable=self.mostrar_quitadas_var,
                                         command=self.atualizar_lista)
        check_quitadas.pack(side="left", padx=20)

        usuario_logado = self.controlador_sistema.usuario_logado
        if usuario_logado and usuario_logado.tipo_usuario == 'administrador':
            btn_adicionar_divida = ttk.Button(controles_frame, text="+ Adicionar Nova Dívida",
                                              command=self.controlador_sistema.controlador_divida.abrir_tela_formulario_divida)
            btn_adicionar_divida.pack(side="right")

            btn_adicionar_recorrencia = ttk.Button(controles_frame, text="+ Adicionar Nova Recorrência",
                                                   command=self.controlador_sistema.controlador_divida.abrir_tela_recorrencia)
            btn_adicionar_recorrencia.pack(side="right", padx=5)

        self.container_lista = ttk.Frame(self.frame_lista_dividas, style="Dividas.TFrame")
        self.container_lista.pack(fill="both", expand=True)

        self.atualizar_lista()

    def _popular_aba_nova_divida(self, container):
        btn_adicionar = ttk.Button(container, text="+ Adicionar Nova Dívida",
                                   command=self.controlador_sistema.controlador_divida.abrir_tela_formulario_divida)
        btn_adicionar.pack(expand=True)

    def atualizar_todas_abas(self):
        self.atualizar_lista()
        self._carregar_conteudo_abas()

    def atualizar_lista(self):
        if not self.container_lista:
            return

        ordenar_por = self.ordenacao_var.get()
        incluir_quitadas = self.mostrar_quitadas_var.get() == 1
        usuario_logado = self.controlador_sistema.usuario_logado

        if usuario_logado:
            tipo_usuario = usuario_logado.tipo_usuario
            self.controlador_sistema.controlador_divida.carregar_dividas_na_view(
                self.container_lista,
                tipo_usuario,
                ordenar_por,
                incluir_quitadas,
                usuario_logado
            )