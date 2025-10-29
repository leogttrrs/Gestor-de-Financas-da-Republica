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
        if not usuario:
            messagebox.showerror("Acesso Negado", "")
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

        ttk.Label(frame, text="Título:").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.titulo_var).pack(fill="x", pady=(0,10))

        ttk.Label(frame, text="Descrição:").pack(anchor="w")
        self.descricao_text = tk.Text(frame, height=6, wrap="word")
        self.descricao_text.pack(fill="both", expand=True, pady=(0,20))

        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill="x", side="bottom")

        btn_salvar = ttk.Button(botoes_frame, text="Salvar", command=self._salvar)
        btn_salvar.pack(side="right", padx=(0,10))

        btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side="right", padx=10)

    def _salvar(self):
        usuario_logado = self.controlador._controlador_sistema.usuario_logado
        try:
            titulo = self.titulo_var.get().strip()
            descricao = self.descricao_text.get("1.0", "end").strip()

            if not titulo or not descricao:
                messagebox.showerror("Erro de Validação", "Preencha todos os campos obrigatórios!", parent=self)
                return

            if self.ocorrencia_existente:
                self.ocorrencia_existente.titulo = titulo
                self.ocorrencia_existente.descricao = descricao
                self.ocorrencia_existente.salvar()
                messagebox.showinfo("Sucesso", "Ocorrência atualizada com sucesso!", parent=self)
            else:
                dados = {
                    "morador": usuario_logado,
                    "titulo": titulo,
                    "descricao": descricao
                }
                sucesso, mensagem = self.controlador.salvar_ocorrencia(dados)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Ocorrência salva com sucesso!", parent=self)
                else:
                    messagebox.showerror("Erro", f"Não foi possível salvar a ocorrência: {mensagem}", parent=self)

            if self.controlador._tela_ocorrencia:
                self.controlador._tela_ocorrencia.atualizar_lista()

            self.destroy()

        except ValueError:
            messagebox.showerror("Erro de Validação", "Apresentou erro", parent=self)


