import tkinter as tk
from tkinter import ttk, messagebox, Toplevel


class TelaAlerta:
    def __init__(self, parent, controlador, eh_admin=False):
        self.parent = parent
        self.controlador = controlador
        self.eh_admin = eh_admin
        self.frame = ttk.Frame(parent)

        self._configurar_estilos()
        self.construir_interface()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Alerta.TFrame", background="white")
        style.configure("Alerta.TLabel", background="white")

        style.configure("Alerta.Card.TFrame", background="white", relief="solid", borderwidth=1)

        style.configure("Alerta.Excluir.TButton",
                        foreground="white",
                        background="#dc3545",
                        borderwidth=0,
                        font=('Arial', 9, 'bold'))
        style.map("Alerta.Excluir.TButton",
                  background=[('active', '#c82333')])

        style.configure("Alerta.Acao.TButton",
                        foreground="white",
                        background="#007bff",
                        borderwidth=0,
                        font=('Arial', 9, 'bold'))
        style.map("Alerta.Acao.TButton", background=[('active', '#0069d9')])

    def construir_interface(self):
        self.frame.configure(style="Alerta.TFrame")

        header_frame = ttk.Frame(self.frame, style="Alerta.TFrame")
        header_frame.pack(fill="x", pady=(0, 20), padx=20)

        lbl_titulo = ttk.Label(header_frame, text="🔔 Mural de Alertas",
                               font=("Arial", 20, "bold"),
                               style="Alerta.TLabel")
        lbl_titulo.pack(side="left")

        if self.eh_admin:
            btn_add = ttk.Button(header_frame, text="+ Novo Alerta",
                                 command=self.abrir_modal_novo_alerta,
                                 style="Alerta.Acao.TButton")
            btn_add.pack(side="right")

        self.canvas = tk.Canvas(self.frame, bd=0, highlightthickness=0, bg="white")
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas, style="Alerta.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")

    def atualizar_lista(self, alertas):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not alertas:
            lbl = ttk.Label(self.scrollable_frame, text="Nenhum alerta publicado.",
                            font=("Arial", 12), foreground="#666", style="Alerta.TLabel")
            lbl.pack(pady=20)
            return

        for alerta in alertas:
            self._criar_card_alerta(alerta)

    def _criar_card_alerta(self, alerta):
        card = ttk.Frame(self.scrollable_frame, style="Alerta.Card.TFrame")
        card.pack(fill="x", pady=10, ipady=5)

        header = ttk.Frame(card, style="Alerta.TFrame")
        header.pack(fill="x", padx=15, pady=(10, 0))

        lbl_data = ttk.Label(header, text=f"📅 {alerta.data_criacao}",
                             font=("Arial", 9, "bold"), foreground="#6c757d",
                             style="Alerta.TLabel")
        lbl_data.pack(side="left")

        if self.eh_admin:
            btn_excluir = ttk.Button(header, text="Excluir",
                                     command=lambda a=alerta: self.controlador.excluir_alerta(a.id),
                                     style="Alerta.Excluir.TButton")
            btn_excluir.pack(side="right")

        lbl_desc = ttk.Label(card, text=alerta.descricao,
                             wraplength=700, justify="left", font=("Arial", 11),
                             style="Alerta.TLabel")
        lbl_desc.pack(fill="x", padx=15, pady=(10, 15))

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def destruir(self):
        self.frame.destroy()

    def abrir_modal_novo_alerta(self):
        modal = Toplevel(self.parent)
        modal.title("Novo Alerta")
        modal.geometry("400x250")
        modal.configure(bg="white")

        ttk.Label(modal, text="Descrição do Alerta:", font=("Arial", 10, "bold"), background="white").pack(anchor="w",
                                                                                                           padx=20,
                                                                                                           pady=(20, 5))

        txt_descricao = tk.Text(modal, height=5, width=40, font=("Arial", 10), relief="solid", borderwidth=1)
        txt_descricao.pack(padx=20, fill="both", expand=True)

        def confirmar():
            descricao = txt_descricao.get("1.0", tk.END).strip()
            if descricao:
                self.controlador.salvar_alerta(descricao)
                modal.destroy()
            else:
                messagebox.showwarning("Atenção", "Digite uma descrição para o alerta.")

        btn_salvar = ttk.Button(modal, text="Publicar", command=confirmar, style="Alerta.Acao.TButton")
        btn_salvar.pack(pady=20)