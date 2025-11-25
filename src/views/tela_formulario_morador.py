import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, StringVar


class TelaFormularioMorador(Toplevel):
    def __init__(self, parent, controlador_morador, callback_cadastrar=None):
        super().__init__(parent)
        self.title("Cadastro de Morador")
        self.geometry("700x420")
        self.configure(bg="#F5F6FA")
        self.resizable(False, False)

        self.controlador_morador = controlador_morador
        self.callback_cadastrar = callback_cadastrar

        self._configurar_estilos()
        self._criar_interface()

        # centralizar
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2 - self.winfo_width() // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2 - self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Card.TFrame", background="white")
        style.configure("Titulo.TLabel", font=("Arial", 20, "bold"), background="#F5F6FA")
        style.configure("Subtitulo.TLabel", font=("Arial", 11), foreground="#555", background="#F5F6FA")
        style.configure("CampoLabel.TLabel", background="white", font=("Arial", 10, "bold"))
        style.configure("CampoEntry.TEntry", padding=6)
        style.configure("BtnAzul.TButton", background="#007bff", foreground="white")
        style.map("BtnAzul.TButton", background=[('active', '#0069d9')])

    def _criar_interface(self):

        ttk.Label(self, text="Cadastro de Morador", style="Titulo.TLabel").pack(
            anchor="w", padx=25, pady=(15, 0)
        )
        ttk.Label(self, text="Preencha os dados para cadastrar um novo morador.",
                  style="Subtitulo.TLabel").pack(anchor="w", padx=25, pady=(0, 15))

        card = ttk.Frame(self, style="Card.TFrame", padding=25)
        card.pack(fill="both", expand=True, padx=20, pady=5)

        self.nome_var = StringVar()
        self.telefone_var = StringVar()
        self.email_var = StringVar()
        self.cpf_var = StringVar()
        self.senha_var = StringVar()

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

        # Nome
        ttk.Label(card, text="Nome completo *", style="CampoLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(card, textvariable=self.nome_var, style="CampoEntry.TEntry")\
            .grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=5)

        # Telefone
        ttk.Label(card, text="Telefone *", style="CampoLabel.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Entry(card, textvariable=self.telefone_var, style="CampoEntry.TEntry")\
            .grid(row=1, column=1, sticky="ew", pady=(0, 15), padx=5)

        # Email
        ttk.Label(card, text="E-mail *", style="CampoLabel.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Entry(card, textvariable=self.email_var, style="CampoEntry.TEntry")\
            .grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=5)

        # CPF
        ttk.Label(card, text="CPF *", style="CampoLabel.TLabel").grid(row=2, column=1, sticky="w")
        ttk.Entry(card, textvariable=self.cpf_var, style="CampoEntry.TEntry")\
            .grid(row=3, column=1, sticky="ew", pady=(0, 15), padx=5)

        # Senha
        ttk.Label(card, text="Senha *", style="CampoLabel.TLabel").grid(row=4, column=0, sticky="w", columnspan=2)
        ttk.Entry(card, textvariable=self.senha_var, style="CampoEntry.TEntry", show="*")\
            .grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)

        # Botões
        botoes = ttk.Frame(card, style="Card.TFrame")
        botoes.grid(row=6, column=0, columnspan=2, sticky="e")

        ttk.Button(botoes, text="Cancelar", command=self.destroy).pack(side="right", padx=5)

        ttk.Button(
            botoes, text="Cadastrar Morador", style="BtnAzul.TButton", command=self._confirmar
        ).pack(side="right")

    def _confirmar(self):
        dados = {
            "nome": self.nome_var.get().strip(),
            "telefone": self.telefone_var.get().strip(),
            "email": self.email_var.get().strip(),
            "cpf": self.cpf_var.get().strip(),
            "senha": self.senha_var.get().strip(),
        }

        # chama o controlador
        sucesso, resultado = self.controlador_morador.cadastrar_morador(dados)

        if not sucesso:
            messagebox.showerror("Erro", resultado)
            return

        messagebox.showinfo("Sucesso", "Morador cadastrado com sucesso!")

        if self.callback_cadastrar:
            self.callback_cadastrar(resultado)

        self.destroy()
