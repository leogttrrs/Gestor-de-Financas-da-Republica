import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.models.Ocorrencia import Ocorrencia
from src.models.Morador import Morador

class TelaFormularioOcorrencia(tk.Toplevel):
    def __init__(self, parent, controlador_ocorrencia, ocorrencia_existente: Ocorrencia = None):
        super().__init__(parent)
        self.controlador = controlador_ocorrencia
        self.ocorrencia_existente = ocorrencia_existente

        usuario = getattr(self.controlador._controlador_sistema, "usuario_logado", None)
        if not usuario or usuario.tipo_usuario != "morador":
            messagebox.showerror("Acesso Negado", "Apenas moradores podem acessar este formulário.")
            self.destroy()
            return

        self.title("Editar Ocorrência" if ocorrencia_existente else "Registrar Ocorrência")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()

        self.morador_var = tk.StringVar()
        self.titulo_var = tk.StringVar()
        self.descricao_var = tk.StringVar()

        self._criar_formulario()

        if ocorrencia_existente:
            self.titulo_var.set(ocorrencia_existente.titulo)
            self.descricao_text.insert("1.0", ocorrencia_existente.descricao)

    def _criar_formulario(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        usuario = self.controlador._controlador_sistema.usuario_logado
        morador_nome = usuario.nome if usuario else ""
        self.morador_var.set(morador_nome)

        ttk.Label(frame, text="Morador:").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.morador_var, state="readonly").pack(fill="x", pady=(0,10))

        ttk.Label(frame, text="Título:").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.titulo_var).pack(fill="x", pady=(0,10))

        ttk.Label(frame, text="Descrição:").pack(anchor="w")
        self.descricao_text = tk.Text(frame, height=6, wrap="word")
        self.descricao_text.pack(fill="both", expand=True, pady=(0,20))

        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill="x", side="bottom")

        ttk.Button(botoes_frame, text="Salvar", command=self._salvar).pack(side="right", padx=(0,10))
        ttk.Button(botoes_frame, text="Cancelar", command=self.destroy).pack(side="right")

    def _salvar(self):
        usuario = getattr(self.controlador._controlador_sistema, "usuario_logado", None)
        if not usuario or usuario.tipo_usuario != "morador":
            messagebox.showerror("Acesso Negado", "Apenas moradores podem acessar este formulário.")
            self.destroy()
            return

        dados = {
            "morador_id": self.controlador._controlador_sistema.usuario_logado.id,
            "titulo": self.titulo_var.get().strip(),
            "descricao": self.descricao_text.get("1.0", "end").strip()
        }

        if not dados['titulo']:
            messagebox.showerror("Erro", "Título é obrigatório.")
            return
        if not dados['descricao']:
            messagebox.showerror("Erro", "Descrição é obrigatória.")
            return

        self.controlador.criar_ocorrencia_interface(dados)

        self.destroy()
