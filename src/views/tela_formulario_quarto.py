import tkinter as tk
from tkinter import ttk, messagebox
from src.models.Quarto import Quarto


class TelaFormularioQuarto(tk.Toplevel):
    def __init__(self, parent, controlador_quarto, quarto_existente: Quarto = None):
        super().__init__(parent)
        self.controlador = controlador_quarto
        self.quarto_existente = quarto_existente

        self.title("Editar Quarto" if quarto_existente else "Adicionar Quarto")
        self.geometry("400x200")
        self.transient(parent)
        self.grab_set()

        self.numero_var = tk.StringVar()
        self.tamanho_var = tk.StringVar()

        self._criar_formulario()
        if quarto_existente:
            self.numero_var.set(str(quarto_existente.numero_quarto))
            self.tamanho_var.set(str(quarto_existente.tamanho))

    def _criar_formulario(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Número do Quarto:").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.numero_var).pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Tamanho (m²):").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.tamanho_var).pack(fill="x", pady=(0, 20))

        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill="x", side="bottom")

        btn_salvar = ttk.Button(botoes_frame, text="Salvar", command=self._salvar)
        btn_salvar.pack(side="right")

        btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side="right", padx=10)

    def _salvar(self):
        try:
            dados = {
                "numero_quarto": int(self.numero_var.get()),
                "tamanho": int(self.tamanho_var.get()),
                "id": self.quarto_existente.id if self.quarto_existente else None
            }
            sucesso, mensagem = self.controlador.salvar_quarto(dados)
            if sucesso:
                messagebox.showinfo("Sucesso", "Quarto salvo com sucesso!", parent=self)
                self.destroy()
            else:
                messagebox.showerror("Erro", f"Não foi possível salvar o quarto: {mensagem}", parent=self)
        except ValueError:
            messagebox.showerror("Erro de Validação", "Número e Tamanho devem ser valores inteiros.", parent=self)